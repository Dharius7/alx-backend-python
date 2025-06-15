from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    unread = models.BooleanField(default=True)

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}: {self.subject}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, related_name='edited_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"History for message {self.message.id} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} regarding message: {self.message.subject}"