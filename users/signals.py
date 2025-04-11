from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User , AuditLog
import logging
   

logger = logging.getLogger(__name__)



def handle_user_registration(sender , instance , created , **kwargs):
    if created:
        logger.info(f"New user registered: {instance.email}")
        print(f"Signal: Welcome email sent to {instance.email}")



