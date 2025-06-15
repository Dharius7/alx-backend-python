from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from . models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a Message is created or updated.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    """
    Signal to create a MessageHistory entry before a Message is updated.
    """
    if instance.pk:
        original_message = Message.objects.get(pk=instance.pk)
        MessageHistory.objects.create(
            message=original_message,
            content=original_message.content,
            edited_by=instance.sender 
        )

@receiver(post_delete, sender=User)
def delete_user_messages(sender, instance, **kwargs):
    """
    Signal to delete all messages related to a User when the User is deleted.
    """
    Message.objects.filter(user=instance).delete()