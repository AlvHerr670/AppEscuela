from django import template
from ..models import Message

register = template.Library()

@register.inclusion_tag('mensajeria/unread_count_badge.html', takes_context=True)
def unread_message_count(context, user):
    count = Message.objects.filter(receiver=user, is_read=False).count()
    return {'unread_count': count}
