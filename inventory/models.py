from django.db import models
from users.models import Company, User
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class AuditLogInventory(models.Model):
    ACTION_CHOICES = [
        ('CREATE',"Create"),
        ("UPDATE","Update"),
        ("DELETE","Delete")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    company = models.ForeignKey(Company , on_delete=models.CASCADE)
    action = models.CharField(max_length= 10 , choices= ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id =  models.PositiveIntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f"{self.user} - {self.action} {self.model_name} (ID: {self.object_id}) at {self.timestamp}"


class AuditLogMixenInventory(models.Model):
    class Meta:
        abstract = True

    def save(self,*args, **kwargs):
        is_new = self._state.adding
        super().save(*args,**kwargs)
        action = "CREATE" if is_new else "UPDATE"
        self.log_action(action)

    def delete(self,*args,**kwargs):
        self.log_action("DELETE")
        super().delete(*args,**kwargs)

    def log_action(self, action):
        AuditLogInventory.objects.create(
            user=self.get_user(),
            company=self.get_company(),
            action=action,
            model_name=self.__class__.__name__,
            object_id=self.id,
            description=str(self)
        )

    def get_user(self):
        return None  # Override in views or dynamically

    def get_company(self):
        return None  


class VehicleInventory( AuditLogMixenInventory,models.Model):
    FUEL_CHOICES = [("PETROL","Petrol"),
                    ("DIESEL"," Diesel"),
                    ("ELECTRIC", "Electric")]

    TRANSMISSION_CHOICES = [("ELECTRIC", "Electric"),
                            ("MANUAL","Manual"),
                            ("AUTOMATIC","Automatic")]

    brand = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory")
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    mileage = models.IntegerField()


    def __str__(self):
        return f"{self.brand} {self.model} ({self.year} - Qty: {self.quantity} - {self.mileage})"
