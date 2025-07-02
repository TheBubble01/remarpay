from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from accounts.permissions import IsTechAdmin, IsManager

# -----------------------------
# Create & Update Exchange Rate
# -----------------------------

class ExchangeRateCreateView(generics.CreateAPIView):
    """
    Create new exchange rate.
    Only Tech Admins or Managers are allowed.
    """
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechAdmin | IsManager]


class ExchangeRateUpdateView(generics.UpdateAPIView):
    """
    Update an existing exchange rate by ID.
    Only Tech Admins or Managers are allowed.
    """
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechAdmin | IsManager]
    lookup_field = 'pk'


# -----------------------------
# View Exchange Rates
# -----------------------------

class ExchangeRateListView(generics.ListAPIView):
    """
    List all exchange rates (ordered by latest update).
    Any authenticated user can view this.
    """
    queryset = ExchangeRate.objects.all().order_by('-updated_at')
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class LatestRatePerCountry(APIView):
    """
    Get the latest exchange rate for a specific country.
    Any authenticated user can view this.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, country):
        rate = ExchangeRate.objects.filter(country=country.lower()).order_by('-updated_at').first()
        if rate:
            serializer = ExchangeRateSerializer(rate)
            return Response(serializer.data)
        return Response({"error": "No rate found for this country."}, status=404)
