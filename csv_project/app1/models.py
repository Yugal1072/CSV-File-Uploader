from django.db import models

# Create your models here.


class Transaction(models.Model):
    invoice_id = models.CharField(max_length=50)
    product_line = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    
    def __str__(self):
        return self.invoice_id
