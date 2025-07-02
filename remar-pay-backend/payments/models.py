from django.db import models
from accounts.models import User

class PaymentRequest(models.Model):
    COUNTRY_CHOICES = [
        ('nigeria', 'Nigeria'),
        ('niger', 'Niger'),
        ('cameroon', 'Cameroon'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    # Submitted by cashier
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_requests')

    # Target destination
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)

    # Deposit info
    deposit_amount_dinar = models.DecimalField(max_digits=10, decimal_places=2)
    fee_applied = models.BooleanField(default=False)
    net_amount_dinar = models.DecimalField(max_digits=10, decimal_places=2)

    # Converted result
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=4)

    # Receiver details
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=30, blank=True)
    receiver_account_number = models.CharField(max_length=50, blank=True)
    receiver_bank_name = models.CharField(max_length=100, blank=True)
    receiver_account_name = models.CharField(max_length=100, blank=True)
    nita_office = models.CharField(max_length=100, blank=True)

    # Depositor details
    depositor_name = models.CharField(max_length=100)
    depositor_phone = models.CharField(max_length=30)

    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Agent actions
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_agent = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='payments_made')
    agent_receipt = models.ImageField(upload_to='agent_receipts/', null=True, blank=True)

    # Cancellation
    is_cancelled = models.BooleanField(default=False)
    cancel_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cashier.name} → {self.country.upper()} ({self.converted_amount})"
