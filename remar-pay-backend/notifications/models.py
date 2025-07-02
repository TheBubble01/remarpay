from django.db import models
from accounts.models import User

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} -> {self.recipient.name}"

