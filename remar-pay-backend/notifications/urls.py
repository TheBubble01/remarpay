from django.urls import path
from .views import (
    SendNotificationView,
    MyNotificationsView,
    MarkNotificationReadView,
    DeleteNotificationView,
)

urlpatterns = [
    # Send notification (Tech Admin / Manager only)
    path('send/', SendNotificationView.as_view(), name='send-notification'),

    # List your own notifications
    path('my/', MyNotificationsView.as_view(), name='my-notifications'),

    # Mark a specific notification as read
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),

    # Delete a specific notification
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='delete-notification'),
]
