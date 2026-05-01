from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(destinataire=request.user, est_lu=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}
