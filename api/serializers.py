from rest_framework import serializers
from .models import User, Contact, Spam
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        """
        Check that the phone number is unique.
        """
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'owner', 'name', 'phone_number', 'is_spam']

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ['id', 'phone_number', 'spam_reports']
        read_only_fields = ['spam_reports']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username 
        token['email'] = user.email

        return token

