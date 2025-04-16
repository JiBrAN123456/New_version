from django.db import models
from inventory.models import VehicleInventory
from users.models import Company
import uuid


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("Sale","SALE"),
        ("Purchase","PURCHASE"),
    ]

    vehicle = models.ForeignKey(VehicleInventory, on_delete=models.CASCADE)
    company = models.ForeignKey(Company , on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=255 , null = True , blank= True)
    seller_name = models.CharField(max_length=255 , null = True , blank= True)
    transaction_type = models.CharField( max_length= 20 , choices=TRANSACTION_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12 , decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True , null=True)

    def __str__(self):
        return f"{self.transaction_type.title()} - {self.vehicle}"
    



class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    transaction = models.OneToOneField(Transaction, on_delete= models.CASCADE)
    invoice_number = models.CharField(max_length=100 , unique=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="invoices/", blank=True , null = True)


    def __str__(self):
        return f"invoice number is {self.invoice_number}"    