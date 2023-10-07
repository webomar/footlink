from django import template
from firstapp.models import Like

register = template.Library()

@register.filter(name='user_has_liked')
def user_has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()
