import random
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import User

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


    def is_valid(self):
        return timezone.now() - self.created_at < timedelta(minutes= 10)

    
    def generate_CODE(self):
        self.code = str(random.randint(100000, 999999))
        self.save()