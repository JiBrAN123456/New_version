from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice, Transaction
from django.utils.crypto import get_random_string
from .utils import generate_invoice_pdf_and_save



@receiver(post_save, sender=Transaction)
def create_invoice_for_transaction(sender, instance, created, **kwargs):
    if created and instance.transaction.type == "sale":
        invoice_number = f"INV-{get_random_string(8).upper()}"
        invoice = Invoice.objects.create(
            transaction = instance,
            invoice_number=invoice_number
        )
        generate_invoice_pdf_and_save(invoice)