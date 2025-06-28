from rest_framework import generics, permissions
from .models import PaymentRequest
from .serializers import PaymentRequestSerializer
from accounts.permissions import IsCashier

class CreatePaymentRequestView(generics.CreateAPIView):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsCashier]

    def get_serializer_context(self):
        # Pass the request object to the serializer
        return {'request': self.request}
