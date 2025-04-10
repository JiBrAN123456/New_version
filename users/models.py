from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.core.exceptions import ValidationError

# Create your models here.

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    name = models.CharField(max_length=255 ,unique=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    ROLE_CHOICES = [ ("admin", "Admin"),
                    ("manager","Manager"),
                    ("staff", "Staff")]
                                         
    name = models.CharField(max_length=50 , choices= ROLE_CHOICES , unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email , password = None ,**extra_fields):
        if not email:
            raise ValueError("Email required")
        
        email = self.normalize(email)

        if not extra_fields.get("is_superuser", False) and not extra_fields.get("company"):
            raise ValueError("Normal users must have a company.")
        
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email , password=None , **extra_fields):
        
        extra_fields.setdefault("is_staff" , True)
        extra_fields.setdefault("Is_superuser" , True)  

        extra_fields.pop("company", None)
        return self.create_user(email, password, company= None , **extra_fields )



class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    company = models.ForeignKey(Company , on_delete=models.CASCADE, null=True, blank=True, related_name="users_company")
    role = models.ForeignKey(Role, on_delete=models.CASCADE , null=True , blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    
    def No_company_for_superuser(self):

        if not self.is_superuser and self.company is None:
            raise ValidationError("Normal users require company")
        super().clean()

    def __str__(self):
        return self.email




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.email , self.user.phone_number, self.user.role , self.user.company 