from django.urls import path
from .views import (
    FundTransferCreateView,
    ConfirmFundTransferView,
    ListFundTransfersView,
)

urlpatterns = [
    path('create/', FundTransferCreateView.as_view(), name='fund_create'),
    path('confirm/<int:pk>/', ConfirmFundTransferView.as_view(), name='fund_confirm'),
    path('list/', ListFundTransfersView.as_view(), name='fund_list'),
]
