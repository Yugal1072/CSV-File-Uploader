from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import *
from .models import *

def home(request):
    return render(request, "base.html")


def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():


            # reading  the CSV file 
            df = pd.read_csv(request.FILES['csv_file'])

            # select only the required columns
            df = df[['Invoice ID', 'Product line', 'Unit price', 'Quantity', 'Tax', 'Total', 'Date', 'Time']]

            # get the first 60 rows
            df = df.iloc[:60]

            # filter transactions for Health and beauty products
            df = df[df['Product line'] == 'Health and beauty']

            # create a list of transaction objects 
            transactions = []
            for index, row in df.iterrows():
                transaction = Transaction(
                    invoice_id=row['Invoice ID'],
                    product_line=row['Product line'],
                    unit_price=row['Unit price'],
                    quantity=row['Quantity'],
                    tax=row['Tax'],
                    total=row['Total'],
                    date=row['Date'],
                    time=row['Time']
                )
                transactions.append(transaction)

            # saving  the transaction obj
            Transaction.objects.bulk_create(transactions)

            # filterng 
            transactions = Transaction.objects.filter(product_line='Health and beauty')
            return render(request, 'transactions.html', {'transactions': transactions})
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def health_beauty_transactions(request):
    transactions = Transaction.objects.filter(product_line__icontains='health and beauty')
    context = {'transactions': transactions}
    return render(request, 'transactions.html', context)