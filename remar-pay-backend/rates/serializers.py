from rest_framework import serializers
from .models import ExchangeRate

class ExchangeRateSerializer(serializers.ModelSerializer):
    """
    Serializer for ExchangeRate model.
    Used for viewing and updating currency exchange rates.
    """
    class Meta:
        model = ExchangeRate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
