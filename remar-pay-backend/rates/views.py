from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from accounts.permissions import IsTechAdmin, IsManager

# Only Tech Admin or Manager can create/update rates
class ExchangeRateCreateView(generics.CreateAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechAdmin | IsManager]

class ExchangeRateUpdateView(generics.UpdateAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechAdmin | IsManager]
    lookup_field = 'pk'

# Anyone authenticated can fetch rates
class ExchangeRateListView(generics.ListAPIView):
    queryset = ExchangeRate.objects.all().order_by('-updated_at')
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated]

# Optionally: latest rate per country
from rest_framework.response import Response
from rest_framework.views import APIView

class LatestRatePerCountry(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, country):
        rate = ExchangeRate.objects.filter(country=country.lower()).order_by('-updated_at').first()
        if rate:
            serializer = ExchangeRateSerializer(rate)
            return Response(serializer.data)
        return Response({"error": "No rate found for this country."}, status=404)
