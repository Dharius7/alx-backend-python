from django.db import models

class MessageQuerySet(models.QuerySet):
    def sent_by(self, user):
        return self.filter(sender=user)

    def received_by(self, user):
        return self.filter(receiver=user)

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def unread_for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            unread=True, 
            parent_message=None
        ).select_related('sender', 'receiver')