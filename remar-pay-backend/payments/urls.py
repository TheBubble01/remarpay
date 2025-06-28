from django.urls import path
from .views import (
    CreatePaymentRequestView,
    AgentPaymentListView,
    MarkPaymentAsPaid,
    UploadReceiptView,
    CreatePaymentRequestView
)

urlpatterns = [
    path('create/', CreatePaymentRequestView.as_view(), name='payment_create'),
    path('agent-list/', AgentPaymentListView.as_view(), name='agent_payments'),
    path('confirm/<int:pk>/', MarkPaymentAsPaid.as_view(), name='confirm_payment'),
    path('upload/<int:pk>/', UploadReceiptView.as_view(), name='upload_receipt'),
    path('cashier/create-request/', CreatePaymentRequestView.as_view(), name='create-payment-request'),
]
