from django import template
from firstapp.models import Like

register = template.Library()

@register.filter(name='is_connected')
def is_connected(user, other_user_id):
    return user.is_connected(other_user_id)



@register.filter(name='user_has_liked')
def user_has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()
