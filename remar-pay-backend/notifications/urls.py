from django.urls import path
from .views import (
    SendNotificationView,
    MyNotificationsView,
    MarkNotificationReadView,
    DeleteNotificationView
)

urlpatterns = [
    path('send/', SendNotificationView.as_view(), name='send-notification'),
    path('my/', MyNotificationsView.as_view(), name='my-notifications'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='delete-notification'),
]
