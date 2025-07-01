from django.urls import path
from .views import CompanyAnalyticsView, UserAnalyticsView

urlpatterns = [
    path('company/', CompanyAnalyticsView.as_view(), name='company-analytics'),
    path('user/', UserAnalyticsView.as_view(), name='user-analytics'),
]