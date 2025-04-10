from django.urls import path
from .views import RegisterUserView, ActivateUserView, VerifyOTPView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate-user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
