from rest_framework import serializers
from .models import FundTransfer

class FundTransferSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.name', read_only=True)

    class Meta:
        model = FundTransfer
        fields = [
            'id', 'sender', 'sender_name',
            'recipient', 'recipient_name',
            'currency', 'amount', 'note',
            'is_confirmed', 'created_at', 'confirmed_at'
        ]
        read_only_fields = ['is_confirmed', 'created_at', 'confirmed_at', 'sender']
