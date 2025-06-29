from django.urls import path
from .views import (
    CreatePaymentRequestView,
    CreatePaymentRequestView
)

urlpatterns = [
    path('create/', CreatePaymentRequestView.as_view(), name='payment_create'),
    path('cashier/create-request/', CreatePaymentRequestView.as_view(), name='create-payment-request'),
]
