from django.contrib.auth.models import get_user_model
from django.http import JsonResponse
from .models import Message
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()

def delete_user(request, user_id):
    """
    View to delete a user and all their related messages.
    """
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User and related messages deleted successfully.'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

def get_threaded_messages(request):
    """
    View to get all threaded messages for the user
    """
    return Message.objects.filter(
        sender=request.user,
        parent_message=None
    ).select_related('sender', 'receiver').prefetch_related('replies__sender', 'replies__receiver').order_by('-timestamp')

def get_unread_messages(request):
    """
    View to get all unread messages for the user
    """
    unread_messages = Message.unread.unread_for_user(request.user).only(
            'id', 'subject', 'content', 'timestamp', 'sender_id', 'receiver_id'
            )
    return JsonResponse({
        'status': 'success',
        'unread_messages': list(unread_messages.values(
            'id', 'subject', 'content', 'timestamp', 'sender__username', 'receiver__username'
        ))
    })

@method_decorator(cache_page(60))
def get_cached_unread_messages(request):
    """
    View to get cached unread messages for the user
    """
    unread_messages = Message.unread.unread_for_user(request.user).only(
            'id', 'subject', 'content', 'timestamp', 'sender_id', 'receiver_id'
            )
    return JsonResponse({
        'status': 'success',
        'unread_messages': list(unread_messages.values(
            'id', 'subject', 'content', 'timestamp', 'sender__username', 'receiver__username'
        ))
    })