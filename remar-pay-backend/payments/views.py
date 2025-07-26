from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from payments.models import PaymentRequest
from payments.serializers import (
    PaymentRequestSerializer,
    AgentPaymentConfirmationSerializer
)
from accounts.permissions import IsCashier

# Cashier: Create new payment request
class CreatePaymentRequestView(generics.CreateAPIView):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer
    permission_classes = [IsAuthenticated, IsCashier]

    def get_serializer_context(self):
        return {'request': self.request}

# Cashier: Generate structured receipt data (used on frontend)
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
            "receiver": {
                "name": payment.receiver_name,
                "phone": payment.receiver_phone,
                "nita_office": payment.nita_office,
            },
            "bank_details": {
                "bank_name": payment.receiver_bank_name,
                "account_number": payment.receiver_account_number,
                "account_name": payment.receiver_account_name,
            },
            "cashier_name": payment.cashier.name,
            "created_at": payment.created_at.strftime('%Y-%m-%d %H:%M'),
        }

        return Response(data)

# Agent: View all unpaid, uncancelled requests for assigned country
class AssignedRequestsListView(generics.ListAPIView):
    serializer_class = PaymentRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentRequest.objects.filter(
            country=self.request.user.assigned_country,
            is_paid=False,
            is_cancelled=False
        ).order_by('-created_at')

# Agent: Confirm payment and upload receipt
class ConfirmPaymentView(generics.UpdateAPIView):
    serializer_class = AgentPaymentConfirmationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentRequest.objects.filter(
            country=self.request.user.assigned_country,
            is_paid=False
        )

    def perform_update(self, serializer):
        serializer.save(
            is_paid=True,
            paid_at=timezone.now(),
            payment_agent=self.request.user
        )

# Cashier: Cancel a request
class CancelPaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            payment = PaymentRequest.objects.get(pk=pk, cashier=request.user)
        except PaymentRequest.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)

        if payment.is_paid:
            return Response({"error": "Cannot cancel a paid request."}, status=400)
        if payment.is_cancelled:
            return Response({"error": "Request already cancelled."}, status=400)

        payment.is_cancelled = True
        payment.cancel_reason = request.data.get('reason', '')
        payment.save()

        return Response({"message": "Request cancelled successfully."}, status=200)

# Search/Filter: Cashiers see their own, agents see theirs
class PaymentRequestSearchView(generics.ListAPIView):
    serializer_class = PaymentRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = PaymentRequest.objects.all()

        # Role-specific visibility
        if user.role == 'cashier':
            qs = qs.filter(cashier=user)
        elif user.role == 'agent':
            qs = qs.filter(payment_agent=user)

        # Filters
        params = self.request.GET
        if params.get('country'):
            qs = qs.filter(country__iexact=params['country'])
        if params.get('is_paid') in ['true', 'false']:
            qs = qs.filter(is_paid=params['is_paid'] == 'true')
        if params.get('is_cancelled') in ['true', 'false']:
            qs = qs.filter(is_cancelled=params['is_cancelled'] == 'true')
        if params.get('cashier_id'):
            qs = qs.filter(cashier__id=params['cashier_id'])
        if params.get('agent_id'):
            qs = qs.filter(payment_agent__id=params['agent_id'])
        if params.get('depositor_phone'):
            qs = qs.filter(depositor_phone__icontains=params['depositor_phone'])
        if params.get('receiver'):
            qs = qs.filter(
                Q(receiver_name__icontains=params['receiver']) |
                Q(receiver_phone__icontains=params['receiver'])
            )
        if params.get('min_amount'):
            qs = qs.filter(deposit_amount_dinar__gte=float(params['min_amount']))
        if params.get('max_amount'):
            qs = qs.filter(deposit_amount_dinar__lte=float(params['max_amount']))

        # Date range filter
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                qs = qs.filter(created_at__range=(start, end))
            except ValueError:
                pass  # Invalid date format

        return qs.order_by('-created_at')

# Cashier: View own transaction history
class CashierTransactionHistoryView(generics.ListAPIView):
    serializer_class = PaymentRequestSerializer
    permission_classes = [IsAuthenticated, IsCashier]

    def get_queryset(self):
        user = self.request.user
        params = self.request.GET
        qs = PaymentRequest.objects.filter(cashier=user)

        # Optional filters
        if params.get('is_paid') in ['true', 'false']:
            qs = qs.filter(is_paid=params['is_paid'] == 'true')
        if params.get('is_cancelled') in ['true', 'false']:
            qs = qs.filter(is_cancelled=params['is_cancelled'] == 'true')
        if params.get('country'):
            qs = qs.filter(country__iexact=params['country'])
        if params.get('depositor_phone'):
            qs = qs.filter(depositor_phone__icontains=params['depositor_phone'])
        if params.get('receiver'):
            qs = qs.filter(
                Q(receiver_name__icontains=params['receiver']) |
                Q(receiver_phone__icontains=params['receiver'])
            )
        if params.get('min_amount'):
            try:
                qs = qs.filter(deposit_amount_dinar__gte=float(params['min_amount']))
            except ValueError:
                pass
        if params.get('max_amount'):
            try:
                qs = qs.filter(deposit_amount_dinar__lte=float(params['max_amount']))
            except ValueError:
                pass
        if params.get('start_date') and params.get('end_date'):
            try:
                start = datetime.strptime(params['start_date'], '%Y-%m-%d')
                end = datetime.strptime(params['end_date'], '%Y-%m-%d')
                qs = qs.filter(created_at__range=(start, end))
            except ValueError:
                pass

        return qs.order_by('-created_at')
