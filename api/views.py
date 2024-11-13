from rest_framework import generics, permissions
from .models import User, Contact, Spam
from .serializers import UserSerializer, ContactSerializer, SpamSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ContactListView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

class SpamMarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            spam, created = Spam.objects.get_or_create(phone_number=phone_number)
            spam.spam_reports += 1  
            spam.save()
            return Response(
                {"message": "Number marked as spam.", "spam_reports": spam.spam_reports},
                status=status.HTTP_200_OK
            )
        return Response({"error": "Phone number not provided."}, status=status.HTTP_400_BAD_REQUEST)

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        phone_number_query = request.query_params.get('phone', '')

        
        if query:
            name_starts_with_results = Contact.objects.filter(name__istartswith=query)
            name_contains_results = Contact.objects.filter(
                Q(name__icontains=query) & ~Q(name__istartswith=query)
            )

            name_results = list(name_starts_with_results) + list(name_contains_results)
            serializer = SpamLikelihoodSerializer(name_results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

       
        elif phone_number_query:
            registered_user = User.objects.filter(phone_number=phone_number_query).first()
            if registered_user:
                serializer = UserSerializer(registered_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                contacts = Contact.objects.filter(phone_number=phone_number_query)
                serializer = SpamLikelihoodSerializer(contacts, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            show_email = False
            if Contact.objects.filter(owner=user, phone_number=request.user.phone_number).exists():
                show_email = True

            user_data = {
                "id": user.id,
                "username": user.username,
                "phone_number": user.phone_number,
                "email": user.email if show_email else None, 
            }

            return Response(user_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
