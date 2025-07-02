from django.db import models

class ExchangeRate(models.Model):
    COUNTRY_CHOICES = [
        ('nigeria', 'Nigeria'),
        ('niger', 'Niger'),
        ('cameroon', 'Cameroon'),
    ]

    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    market_rate = models.DecimalField(max_digits=10, decimal_places=2)
    remar_rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(max_length=10)  # e.g. NGN, XOF, XAF

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.country.title()} - Remar Rate: {self.remar_rate}"
