from django.urls import path
from .views import RegistrationView, UserLoginView, user_logout, activate, UserProfileUpdateView
urlpatterns = [
    path('signup/', RegistrationView, name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('user_update/<int:pk>/',
         UserProfileUpdateView.as_view(), name='user_update'),
    path('logout/', user_logout, name='user_logout'),
    path('signup/<uid64>/<token>/', activate, name='activate'),

]
