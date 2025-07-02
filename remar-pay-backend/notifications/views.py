from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from accounts.models import User
from accounts.permissions import IsTechAdmin, IsManager

# Send notification to specific user or all users in a role
class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin | IsManager]

    def post(self, request):
        title = request.data.get('title')
        message = request.data.get('message')
        recipient_id = request.data.get('recipient_id')
        role = request.data.get('role')

        if not title or not message:
            return Response({"error": "Title and message are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Send to a single user
        if recipient_id:
            try:
                recipient = User.objects.get(id=recipient_id)
                Notification.objects.create(title=title, message=message, recipient=recipient)
                return Response({"message": f"Notification sent to {recipient.name}"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Send to all users in a specific role
        elif role:
            users = User.objects.filter(role=role)
            if not users.exists():
                return Response({"error": f"No users found with role '{role}'."}, status=status.HTTP_404_NOT_FOUND)
            notifications = [
                Notification(title=title, message=message, recipient=user) for user in users
            ]
            Notification.objects.bulk_create(notifications)
            return Response({"message": f"Notification sent to all {role}s."}, status=status.HTTP_200_OK)

        return Response({"error": "Provide either 'recipient_id' or 'role'."}, status=status.HTTP_400_BAD_REQUEST)


# Authenticated users fetch their own notifications
class MyNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Mark a notification as read
class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, recipient=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)


# Delete a notification
class DeleteNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, recipient=request.user)
            notification.delete()
            return Response({"message": "Notification deleted."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
