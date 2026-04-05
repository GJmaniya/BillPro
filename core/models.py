from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    billing_date = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00) # GST percentage
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='bills/pdf/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate total amount
        gst_amount = (self.price * self.gst_rate) / Decimal('100.00')
        self.total_amount = self.price + gst_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.id} - {self.project_name} for {self.client_name}"

class Challan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name='challan', blank=True, null=True)
    project_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    delivery_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='challans/pdf/', blank=True, null=True)

    def __str__(self):
        return f"Challan {self.id} - {self.project_name}"
