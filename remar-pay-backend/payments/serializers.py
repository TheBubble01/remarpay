from rest_framework import serializers
from .models import PaymentRequest
from accounts.models import User
from rates.models import ExchangeRate  # Holds remar_rate for each country


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        exclude = ['status', 'cashier', 'created_at']  # System-managed fields
        read_only_fields = ['net_amount_dinar', 'converted_amount', 'conversion_rate', 'fee_applied']

    def validate(self, data):
        country = data.get('country')
        deposit_amount = data.get('deposit_amount_dinar')

        # Validate required fields based on country rules
        if country == 'nigeria':
            required = ['receiver_bank_name', 'receiver_account_number', 'receiver_account_name']
        elif country in ['niger', 'cameroon']:
            required = ['nita_office']
        else:
            raise serializers.ValidationError("Unsupported country selected.")

        for field in required:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required for selected country."})

        return data

    def create(self, validated_data):
        request = self.context['request']
        country = validated_data['country']
        deposit_amount = validated_data['deposit_amount_dinar']

        # 5 Dinar fee logic (for amounts < 500)
        fee_applied = deposit_amount < 500
        net_amount = deposit_amount - 5 if fee_applied else deposit_amount

        # Get remar_rate from ExchangeRate
        try:
            rate = ExchangeRate.objects.get(country=country)
            conversion_rate = rate.remar_rate
        except ExchangeRate.DoesNotExist:
            raise serializers.ValidationError("Conversion rate not set for the selected country.")

        converted = net_amount * conversion_rate

        return PaymentRequest.objects.create(
            cashier=request.user,
            country=country,
            deposit_amount_dinar=deposit_amount,
            net_amount_dinar=net_amount,
            fee_applied=fee_applied,
            converted_amount=converted,
            conversion_rate=conversion_rate,

            # Receiver fields
            receiver_name=validated_data['receiver_name'],
            receiver_phone=validated_data.get('receiver_phone', ''),
            receiver_account_number=validated_data.get('receiver_account_number', ''),
            receiver_bank_name=validated_data.get('receiver_bank_name', ''),
            receiver_account_name=validated_data.get('receiver_account_name', ''),
            nita_office=validated_data.get('nita_office', ''),

            # Depositor fields
            depositor_name=validated_data['depositor_name'],
            depositor_phone=validated_data['depositor_phone'],
        )


class AgentPaymentConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ['is_paid', 'agent_receipt']
        extra_kwargs = {
            'is_paid': {'required': True},
            'agent_receipt': {'required': False},
        }
