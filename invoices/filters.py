import django_filters
from .models import Transaction



class TransactionFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price" , lookup_expr="lte")
    start_date = django_filters.DateFilter( field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter( field_name= "date", lookup_expr= "lte")
    transaction_type = django_filters.CharFilter( field_name="transaction_type", lookup_expr="iexact")

    class Meta:
        model = Transaction
        fields = ['transaction_type','vehicle','company'] 