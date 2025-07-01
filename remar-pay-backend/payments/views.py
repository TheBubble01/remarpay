from rest_framework import generics, permissions
from .models import PaymentRequest
from .serializers import PaymentRequestSerializer, AgentPaymentConfirmationSerializer
from accounts.permissions import IsCashier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils.receipt_generator import generate_receipt_image
from django.utils import timezone


class CreatePaymentRequestView(generics.CreateAPIView):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsCashier]

    def get_serializer_context(self):
        # Pass the request object to the serializer
        return {'request': self.request}

class GenerateReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            payment = PaymentRequest.objects.get(pk=pk, cashier=request.user)
        except PaymentRequest.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)

        data = {
            "id": payment.id,
            "country": payment.country,
            "depositor_name": payment.depositor_name,
            "depositor_phone": payment.depositor_phone,
            "deposit_amount_dinar": float(payment.deposit_amount_dinar),
            "converted_amount": float(payment.converted_amount),
            "conversion_rate": float(payment.conversion_rate),
            "fee_applied": payment.fee_applied,

            # Conditional fields
            "receiver": {
                "name": payment.receiver_name,
                "phone": payment.receiver_phone,
                "nita_office": getattr(payment, 'nita_office', None),
            },
            "bank_details": {
                "bank_name": getattr(payment, 'receiver_bank_name', None),
                "account_number": getattr(payment, 'receiver_account_number', None),
                "account_name": getattr(payment, 'receiver_account_name', None),
            },
            "cashier_name": payment.cashier.name,
            "created_at": payment.created_at.strftime('%Y-%m-%d %H:%M')
        }

        return Response(data)
    
# Agent's end:
# List assigned country requests
class AssignedRequestsListView(generics.ListAPIView):
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PaymentRequest.objects.filter(
            country=user.assigned_country,
            is_paid=False,
            is_cancelled=False
        ).order_by('-created_at')

# Confirm a payment (mark as paid)
class ConfirmPaymentView(generics.UpdateAPIView):
    serializer_class = AgentPaymentConfirmationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PaymentRequest.objects.filter(
            country=user.assigned_country,
            is_paid=False
        )

    def perform_update(self, serializer):
        serializer.save(
            is_paid=True,
            paid_at=timezone.now(),
            payment_agent=self.request.user
        )

# Cancelled order
class CancelPaymentRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            payment = PaymentRequest.objects.get(pk=pk, cashier=request.user)
        except PaymentRequest.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)

        if payment.is_paid:
            return Response({"error": "Cannot cancel a paid request."}, status=400)

        if payment.is_cancelled:
            return Response({"error": "Request already cancelled."}, status=400)

        reason = request.data.get('reason', '')
        payment.is_cancelled = True
        payment.cancel_reason = reason
        payment.save()

        return Response({"message": "Request cancelled successfully."}, status=200)
    
   