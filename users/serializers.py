from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .models import User, Company, Role, Profile
from .OTP import OTP
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","company","role"]



class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only = True)
    company = serializers.PrimaryKeyRelatedField(queryset= Company.objects.all(), required = False)
    role = serializers.PrimaryKeyRelatedField(queryset= Role.objects.all() , required =False) 


    class Meta:
        model = User
        fields = ["email" , 'password' , "phone_number" , 'company', 'role']


    def validate(self , data):
        if not data.get("company"):
            raise serializers.ValidationError("Company is required for normal users")
        return data


    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        Profile.objects.create(user=user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator(user)
        link = f"http://localhost:8000/api/activate/{uid}/{token}/"
        send_mail(
            "Verify your email",
            f"Click to verify: {link}",
            "noreply@yourdomain.com",
            [user.email],
        )


        otp_obj, _ = OTP.objects.get_or_create(user=user)
        otp_obj.generate_CODE()
        send_mail(
            "Your OTP Code",
            f"Use this OTP to finish registration: {otp_obj.code}",
            "noreply@yourdomain.com",
            [user.email],
        )
        return user    
    


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only= True) 

    def validate(self, data):
        email = data.get('email')
        password = data.get("password")

        user = authenticate(email= email , password=password)
        if not user:
            raise serializers.ValidationError("not valid user or password")
        
        refresh = RefreshToken.for_user(user)

        return{
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
            "user": UserSerializer(user).data
        }
    

class ProfileSerializer(serializers.ModelSerializer):    

    user_email = serializers.EmailField(source = 'user.email', read_only = True)
    user_company = serializers.CharField(source = 'user.company.name' , read_only = True)
    user_role = serializers.CharField(source = "role.name", read_only = True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True) 
    
    class Meta:
        model = Profile
        fields = ["user" ,"user_email", "user_company", "user_role", "phone_number" , "created_at", "modified_at"]

  