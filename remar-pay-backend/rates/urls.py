from django.urls import path
from .views import (
    ExchangeRateCreateView,
    ExchangeRateUpdateView,
    ExchangeRateListView,
    LatestRatePerCountry,
)

urlpatterns = [
    # Create a new exchange rate
    path('create/', ExchangeRateCreateView.as_view(), name='create_rate'),

    # Update an existing rate by ID
    path('update/<int:pk>/', ExchangeRateUpdateView.as_view(), name='update_rate'),

    # List all rates (for dashboard or records)
    path('list/', ExchangeRateListView.as_view(), name='list_rates'),

    # Fetch the latest rate for a specific country
    path('latest/<str:country>/', LatestRatePerCountry.as_view(), name='latest_rate_country'),
]
