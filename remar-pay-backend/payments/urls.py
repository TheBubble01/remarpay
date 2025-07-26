from django.urls import path
from .views import (
    CreatePaymentRequestView,
    GenerateReceiptView,
    AssignedRequestsListView,
    ConfirmPaymentView,
    CancelPaymentRequestView,
    PaymentRequestSearchView, 
    CashierTransactionHistoryView,  
)

urlpatterns = [
    # Cashier endpoints
    path('cashier/create-request/', CreatePaymentRequestView.as_view(), name='create-payment-request'),
    path('cashier/receipt/<int:pk>/', GenerateReceiptView.as_view(), name='generate-receipt'),
    path('cashier/cancel/<int:pk>/', CancelPaymentRequestView.as_view(), name='cancel-payment'),
    path('cashier/history/', CashierTransactionHistoryView.as_view(), name='cashier-transaction-history'), # name='cashier-history'
    
    # Agent endpoints
    path('agent/requests/', AssignedRequestsListView.as_view(), name='agent-requests'),
    path('agent/confirm/<int:pk>/', ConfirmPaymentView.as_view(), name='confirm-payment'),

    # Shared utilities
    path('search/', PaymentRequestSearchView.as_view(), name='payment_search'),
]
