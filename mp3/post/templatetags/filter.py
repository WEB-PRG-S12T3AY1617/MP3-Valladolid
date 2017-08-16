from django import template

from post.models import User

register = template.Library()

@register.filter
def getUserName(userId):
    try:
        user = User.objects.get(pk=userId)
    except User.DoesNotExist:
        return None

    return user.user_name

@register.filter
def getUser(sessions):
    if 'uid' in sessions:
        return sessions['uid']
    else:
        return None

@register.filter
def getType(obj):
    return type(obj).__name__