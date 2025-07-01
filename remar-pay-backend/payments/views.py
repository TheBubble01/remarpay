from rest_framework import generics, permissions
from payments.models import PaymentRequest
from payments.serializers import PaymentRequestSerializer, AgentPaymentConfirmationSerializer
from accounts.permissions import IsCashier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from payments.utils.receipt_generator import generate_receipt_image
from django.utils import timezone
from django.db.models import Sum, Q
from django.utils.dateparse import parse_date
# from accounts.models import User
from rates.models import ExchangeRate

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
    
# Analytics
class CompanyAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all successful requests (not cancelled)
        requests = PaymentRequest.objects.filter(is_cancelled=False, is_paid=True)

        summary = {
            "total_dinar_collected": 0,
            "fixed_fee_profit_dinar": 0,
            "exchange_margin_profit_dinar": 0,
            "total_estimated_profit_dinar": 0,
            "num_successful_requests": requests.count(),
            "num_cancelled_requests": PaymentRequest.objects.filter(is_cancelled=True).count(),
            "outstanding_balance_estimate": 0,
        }

        per_currency = {}
        total_sent_by_agents = 0
        total_margin_profit_dinar = 0
        fixed_fee_dinar = PaymentRequest.objects.filter(fee_applied=True).count() * 5

        for country_code in ['nigeria', 'niger', 'cameroon']:
            country_requests = requests.filter(country=country_code)
            if not country_requests.exists():
                continue

            try:
                rate_obj = ExchangeRate.objects.get(country=country_code)
            except ExchangeRate.DoesNotExist:
                continue

            total_sent = country_requests.aggregate(total=Sum('converted_amount'))['total'] or 0
            currency = rate_obj.currency_code
            margin_profit_local = 0
            margin_profit_dinar = 0

            for req in country_requests:
                if req.conversion_rate and req.net_amount_dinar:
                    try:
                        market_rate = ExchangeRate.objects.get(country=req.country).market_rate
                        margin = (market_rate - req.conversion_rate) * req.net_amount_dinar
                        margin_profit_local += margin
                        # Convert this margin back to Dinar
                        margin_profit_dinar += (margin / req.conversion_rate)
                    except:
                        continue

            total_sent_by_agents += total_sent
            total_margin_profit_dinar += margin_profit_dinar

            per_currency[country_code] = {
                "currency": currency,
                "total_sent_by_agents": total_sent,
                "exchange_margin_profit_local": round(margin_profit_local, 2),
                "converted_back_to_dinar": round(margin_profit_dinar, 2),
            }

        summary["total_dinar_collected"] = PaymentRequest.objects.aggregate(
            total=Sum('deposit_amount_dinar'))['total'] or 0

        summary["fixed_fee_profit_dinar"] = fixed_fee_dinar
        summary["exchange_margin_profit_dinar"] = round(total_margin_profit_dinar, 2)
        summary["total_estimated_profit_dinar"] = round(total_margin_profit_dinar + fixed_fee_dinar, 2)

        # Estimate balance = dinar collected - equivalent sent
        total_net_dinar = requests.aggregate(total=Sum('net_amount_dinar'))['total'] or 0
        summary["outstanding_balance_estimate"] = round(summary["total_dinar_collected"] - total_net_dinar, 2)

        return Response({
            "summary": summary,
            "per_currency": per_currency
        })
