from django.urls import path
from .views import download_invoice_pdf, sales_purchases_summary , TransactionListView , DashboardView

urlpatterns = [
    path('download/<uuid:invoice_id>/', download_invoice_pdf, name='download_invoice_pdf'),
    path('summary/', sales_purchases_summary, name='sales_purchases_summary'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
]


