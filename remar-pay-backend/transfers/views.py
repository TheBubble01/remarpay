from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import FundTransfer
from .serializers import FundTransferSerializer
from accounts.permissions import IsTechAdmin, IsManager, IsAgent
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

# Manager or TechAdmin creates the transfer
class FundTransferCreateView(generics.CreateAPIView):
    queryset = FundTransfer.objects.all()
    serializer_class = FundTransferSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager | IsTechAdmin]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# Agent confirms receipt of fund (single transfer)
class ConfirmFundTransferView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAgent | IsTechAdmin]

    def post(self, request, pk):
        try:
            transfer = FundTransfer.objects.get(id=pk, recipient=request.user)
            if transfer.is_confirmed:
                return Response({"detail": "Transfer already confirmed."}, status=400)
            transfer.is_confirmed = True
            transfer.confirmed_at = timezone.now()
            transfer.save()
            return Response({"message": "Transfer confirmed successfully."})
        except FundTransfer.DoesNotExist:
            return Response({"error": "Transfer not found or unauthorized."}, status=404)

# Manager/TechAdmin views all transfers
class ListFundTransfersView(generics.ListAPIView):
    queryset = FundTransfer.objects.all().order_by('-created_at')
    serializer_class = FundTransferSerializer
    permission_classes = [permissions.IsAuthenticated]
