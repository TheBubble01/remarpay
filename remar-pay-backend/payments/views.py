from rest_framework import generics, permissions
from .models import PaymentRequest
from .serializers import PaymentRequestSerializer
from accounts.permissions import IsCashier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from .utils.receipt_generator import generate_receipt_image
import os

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

        # Generate file path
        filename = f"receipt_{payment.pk}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, 'receipts', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Generate image
        generate_receipt_image(payment, file_path)

        # Return downloadable image
        return FileResponse(open(file_path, 'rb'), content_type='image/png')
