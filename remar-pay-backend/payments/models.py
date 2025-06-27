from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class PaymentRequest(models.Model):
    COUNTRY_CHOICES = [
        ('nigeria', 'Nigeria'),
        ('niger', 'Niger'),
        ('cameroon', 'Cameroon'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_payments')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_requests')
    
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    amount_dinar = models.DecimalField(max_digits=12, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee_deducted = models.BooleanField(default=False)

    payment_details = models.JSONField()  # Flexible for country-specific fields

    receipt_image = models.ImageField(upload_to='client_receipts/', null=True, blank=True)
    agent_payment_receipt = models.ImageField(upload_to='agent_receipts/', null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cashier.name} → {self.country.upper()} | {self.converted_amount} | {self.status}"
