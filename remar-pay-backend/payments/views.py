from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import PaymentRequest
from .serializers import PaymentRequestSerializer
from accounts.permissions import IsCashier, IsAgent
from accounts.models import User  # to filter agents
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

# Create payment request (Cashier only)
class CreatePaymentRequestView(generics.CreateAPIView):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsCashier]

    def perform_create(self, serializer):
        country = self.request.data.get('country')
        try:
            agent = User.objects.get(role='agent', assigned_country=country)
        except User.DoesNotExist:
            agent = None
        serializer.save(cashier=self.request.user, agent=agent)

# Agent views all requests assigned to them
class AgentPaymentListView(generics.ListAPIView):
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgent]

    def get_queryset(self):
        return PaymentRequest.objects.filter(agent=self.request.user).order_by('-created_at')

# Agent confirms payment (marks as paid)
class MarkPaymentAsPaid(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAgent]

    def post(self, request, pk):
        try:
            payment = PaymentRequest.objects.get(pk=pk, agent=request.user)
            if payment.status == 'paid':
                return Response({"message": "Already marked as paid."})
            payment.status = 'paid'
            payment.paid_at = timezone.now()
            payment.save()
            return Response({"message": "Payment marked as paid."})
        except PaymentRequest.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)

# Receipt upload endpoints (cashier or agent can PATCH anytime)
class UploadReceiptView(generics.UpdateAPIView):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]  # We'll check specific role in frontend
    http_method_names = ['patch']
