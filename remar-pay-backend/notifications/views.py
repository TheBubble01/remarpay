from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from accounts.models import User
from accounts.permissions import IsTechAdmin, IsManager
from django.db.models import Q

# Send notification to user(s)
class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin | IsManager]

    def post(self, request):
        title = request.data.get('title')
        message = request.data.get('message')
        recipient_id = request.data.get('recipient_id')
        role = request.data.get('role')

        if not title or not message:
            return Response({"error": "Title and message are required."}, status=400)

        if recipient_id:
            try:
                recipient = User.objects.get(id=recipient_id)
                Notification.objects.create(title=title, message=message, recipient=recipient)
                return Response({"message": f"Notification sent to {recipient.name}"})
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=404)

        elif role:
            users = User.objects.filter(role=role)
            for user in users:
                Notification.objects.create(title=title, message=message, recipient=user)
            return Response({"message": f"Notification sent to all {role}s."})

        return Response({"error": "Provide either recipient_id or role."}, status=400)


# List your notifications
class MyNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


# Mark as read
class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, recipient=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read."})
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=404)


# Delete a notification
class DeleteNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, recipient=request.user)
            notification.delete()
            return Response({"message": "Notification deleted."})
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=404)
