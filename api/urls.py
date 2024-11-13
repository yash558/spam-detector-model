from django.urls import path
from .views import RegisterUserView, ContactListView, SpamMarkView, SearchView , RegisterUserView, UserProfileView, UserDetailsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('contacts/mark-spam/', SpamMarkView.as_view(), name='mark-spam'),
    path('search/', SearchView.as_view(), name='search'), 
    path('user/<int:user_id>/', UserDetailsView.as_view(), name='user-details'), 
    path('profile/', UserProfileView.as_view(), name='profile'),
    
]
