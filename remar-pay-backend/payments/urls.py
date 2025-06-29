from django.urls import path
from .views import (
    CreatePaymentRequestView,
    CreatePaymentRequestView,
    GenerateReceiptView
)

urlpatterns = [
    path('create/', CreatePaymentRequestView.as_view(), name='payment_create'),
    path('cashier/create-request/', CreatePaymentRequestView.as_view(), name='create-payment-request'),
    path('cashier/receipt/<int:pk>/', GenerateReceiptView.as_view(), name='generate-receipt'),
]

