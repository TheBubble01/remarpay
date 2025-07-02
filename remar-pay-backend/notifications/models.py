from django.db import models
from accounts.models import User

class Notification(models.Model):
    """
    Stores a notification sent to a specific user.
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Truncate long titles for cleaner admin output
        return f"To {self.recipient.name}: {self.title[:30]}{'...' if len(self.title) > 30 else ''}"
