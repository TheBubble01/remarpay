from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from payments.models import PaymentRequest
from django.db.models import Sum, Count, Q
from rates.models import ExchangeRate
from django.utils import timezone
from datetime import datetime

# Company-level analytics
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

# User-level Analytics
class UserAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')

        filters = Q()
        if start and end:
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                end_date = datetime.strptime(end, "%Y-%m-%d")
                filters &= Q(created_at__range=(start_date, end_date))
            except:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        data = {
            "user": user.name,
            "role": user.role,
        }

        if role == "cashier":
            my_requests = PaymentRequest.objects.filter(cashier=user).filter(filters)

            total_requests = my_requests.count()
            successful = my_requests.filter(is_paid=True, is_cancelled=False).count()
            cancelled = my_requests.filter(is_cancelled=True).count()
            total_dinar_received = my_requests.aggregate(Sum('deposit_amount_dinar'))['deposit_amount_dinar__sum'] or 0
            converted_by_country = my_requests.values('country').annotate(
            total=Sum('converted_amount')
            )
            converted_totals = {}
            for item in converted_by_country:
                country = item['country']
                rate = ExchangeRate.objects.filter(country=country).first()
                currency = rate.currency_code if rate else "???"
                converted_totals[country] = {
                    "currency": currency,
                    "amount": item['total']
                }

            data.update({
                "total_requests": total_requests,
                "successful_requests": successful,
                "cancelled_requests": cancelled,
                "total_dinar_collected": total_dinar_received,
                "total_converted": converted_totals,
            })

        elif role == "agent":
            my_requests = PaymentRequest.objects.filter(payment_agent=user).filter(filters)

            total_paid = my_requests.filter(is_paid=True).count()
            total_pending = my_requests.filter(is_paid=False, is_cancelled=False).count()
            #total_amount_sent = my_requests.filter(is_paid=True).aggregate(Sum('converted_amount'))['converted_amount__sum'] or 0

            sent_by_country = my_requests.filter(is_paid=True).values('country').annotate(
                total=Sum('converted_amount')
            )

            sent_totals = {}
            for item in sent_by_country:
                country = item['country']
                rate = ExchangeRate.objects.filter(country=country).first()
                currency = rate.currency_code if rate else "???"
                sent_totals[country] = {
                    "currency": currency,
                    "amount": item['total']
                }

            data.update({
                "total_paid_requests": total_paid,
                "total_pending_requests": total_pending,
                "total_sent": sent_totals,
            })

        elif role in ["manager", "tech-admin"]:
            # Show some high-level stats if needed
            data.update({
                "message": "Managers have access to company-level analytics only."
            })

        return Response(data)
