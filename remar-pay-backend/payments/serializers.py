from rest_framework import serializers
from .models import PaymentRequest

class PaymentRequestSerializer(serializers.ModelSerializer):
    cashier_name = serializers.CharField(source='cashier.name', read_only=True)
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    receipt_image = serializers.ImageField(required=False)
    agent_payment_receipt = serializers.ImageField(required=False)

    class Meta:
        model = PaymentRequest
        fields = [
            'id', 'cashier', 'cashier_name', 'agent', 'agent_name',
            'country', 'amount_dinar', 'converted_amount', 'fee_deducted',
            'payment_details', 'receipt_image', 'agent_payment_receipt',
            'status', 'created_at', 'paid_at'
        ]
        read_only_fields = ['cashier', 'agent', 'status', 'paid_at', 'created_at']
