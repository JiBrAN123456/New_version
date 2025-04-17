from django.http import FileResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Invoice, Transaction



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