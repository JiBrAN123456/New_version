from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserRegistrationSerializer


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh':str(refresh),
            "access" : str(refresh.access_token)}


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Check your email fro verification and OTP"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class ActivaterUserVieq(APIView):
    def get(self ,request,uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except Exception:
            return Response({"error": "Invalid activation link"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"})
        return Response({"error": "Invalid or expired token"}, status=400)
    
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        user = get_object_or_404(User, email=email)

        otp_obj = getattr(user, "otp", None)
        if not otp_obj or otp_obj.code != otp or not otp_obj.is_valid():
            return Response({"error": "Invalid or expired OTP"}, status=400)

        otp_obj.delete()  # Optional: remove OTP after success
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "2FA complete. You are now logged in.",
            "tokens": tokens
        }, status=200)