from django.contrib import admin
from .models import Transaction, Invoice

admin.site.register(Transaction)
admin.site.register(Invoice)
