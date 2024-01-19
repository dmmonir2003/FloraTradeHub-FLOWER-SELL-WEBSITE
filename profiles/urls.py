from django.urls import path
from .views import RegistrationView, UserLoginView, UserLogOutView, activate, UserProfileUpdateView
urlpatterns = [
    path('signup/', RegistrationView, name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('user_update/<int:pk>/',
         UserProfileUpdateView.as_view(), name='user_update'),
    path('logout/', UserLogOutView.as_view(), name='user_logout'),
    path('signup/<uid64>/<token>/', activate, name='activate'),

]
