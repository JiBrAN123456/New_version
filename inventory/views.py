from rest_framework import viewsets, permissions
from .models import VehicleInventory
from .serializers import VehicleInventorySerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import Q
# Create your views here.

class VehiclePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        try:
           return super().paginate_queryset(queryset, request, view)
        except NotFound:
             self.page = None
             return []

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count if self.page else 0,
            'results': data
        })


class VehicleInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VehicleInventorySerializer
    pagination_class = VehiclePagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend , OrderingFilter , SearchFilter]

    filter_fields = ['brand' , 'year', "fuel_type"]
    ordering_fields = ["year", 'brand' , "price"]
    search_fields = ["brand","model"]


    def get_queryset(self):
        queryset = VehicleInventory.objects.filter(company = self.request.user.company)
        
        min_year = self.request.query_params.get("year__gte")
        max_year = self.request.query_params.get("year__lte")

        if min_year:
            queryset = queryset.filter(year__gte=min_year)
        if max_year:
            queryset = queryset.filter(year__gte=max_year)    
        
        search_query = self.request.query_params.get("search")
        if search_query:
           queryset = queryset.filter(
               Q(brand__icontains=search_query) |
               Q(model__icontains=search_query)
           )

        return queryset