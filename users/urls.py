from django.urls import path
from .views import RegistrationView , ActivaterUserView, VerifyOTPView, LogoutView, CustomLoginView , ProfileView




urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivaterUserView.as_view(), name='activate-user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
     path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("profile/", ProfileView.as_view(), name="profile"),


]
