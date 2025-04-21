from django.http import FileResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Invoice, Transaction
from rest_framework.generics import ListAPIView
from .serializers import TransactionSerializer
from .filters import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count , Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from datetime import datetime
from rest_framework.views import APIView



def download_invoice_pdf(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        return FileResponse(invoice.pdf_file.open('rb'), content_type="application/pdf")
    except Invoice.DoesNotExist:
        raise Http404("invoice not found")
    

@api_view(["GET"])
def sales_purchases_summary(request):
    sales_count = Transaction.objects.filter(transaction_type0 ='sale').count()
    purchase_count = Transaction.objects.filter(transaction_type = "purchase").count()


    return Response({
        "labels": ['Sales',"Purchases"],
        'data': [sales_count, purchase_count]
    }) 




class TransactionListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TransactionFilter
    search_fields = ['buyer_name', 'seller_name', 'vehicle__vin', 'vehicle__model']
    ordering_fields = ['date', 'price']




class DashboardView(APIView):
      
      def get(self,request):
          chart_type = request.query_params.get("type")

          if chart_type == "sales_trend":
              return self.sales_trend(request)
          elif chart_type == "top_models":
              return self.top_models(request)
          elif chart_type == "monthly_revenue":
              return self.monthly_revenue(request)
          else:
              return Response({"error": "Invalid request"}, status=400) 
          
      def sales_trend(self,request):
          granularity = request.query_params.get("granularity","day")
          truncate = {
              "day": TruncDay("date"),
              "week": TruncWeek("date"),
              "month": TruncMonth("date")
          }.get(granularity, TruncDay("date"))


          data = (
              Transaction.objects.filter(transaction_type ="sale")
              .annotate(period=truncate)
              .values("period")
              .annotate(count=Count("id"))
              .order_by("period")
          )


          return Response(data)

      def top_models(self,request):
          data = (Transaction.objects.filter(transaction_type="sale")
                  .annotate(month=TruncMonth("date"))
                  .values("month")
                  .annotate(total_revenue=Sum("price"))
                  .order_by("month")
                  
                  )
          
          return Response(data)

      def monthly_revenue(self,request):    
           data = (
            Transaction.objects.filter(transaction_type="sale")
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total_revenue=Sum("price"))
            .order_by("month"))
           return Response(data)
