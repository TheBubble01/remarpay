from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for delivering notifications to the frontend.
    Fields like 'id', 'created_at', and 'is_read' are read-only.
    """
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_read']
