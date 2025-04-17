from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleInventoryViewSet
   )


router = DefaultRouter()
router.register(r'master-inventory', VehicleInventoryViewSet, basename='vehicle-master')



urlpatterns = [
    path('', include(router.urls)),  # Include all registered endpoints
    path('invoices/', include('invoices.urls')),
]
