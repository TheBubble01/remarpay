from django.urls import path
from .views import (
    ExchangeRateCreateView,
    ExchangeRateUpdateView,
    ExchangeRateListView,
    LatestRatePerCountry,
)

urlpatterns = [
    path('create/', ExchangeRateCreateView.as_view(), name='create_rate'),
    path('update/<int:pk>/', ExchangeRateUpdateView.as_view(), name='update_rate'),
    path('list/', ExchangeRateListView.as_view(), name='list_rates'),
    path('latest/<str:country>/', LatestRatePerCountry.as_view(), name='latest_rate_country'),
]
