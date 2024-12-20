from django import template
from django.utils.html import format_html
from accounts.models import Profile

register = template.Library()

@register.simple_tag
def user_avatar(user, size=40):
    """
    Renders a user's avatar or a default circle with their first initial.
    Usage: {% user_avatar user 40 %}
    """
    try:
        if hasattr(user, 'user_profile'):
            profile = user.user_profile
            if profile and profile.avatar:
                return format_html(
                    '<img src="{}" class="rounded-circle" width="{}" height="{}" alt="{}">',
                    profile.avatar.url, size, size, user.username
                )
    except (Profile.DoesNotExist, AttributeError):
        pass
    
    # Default avatar with initial
    font_size = size // 2
    return format_html(
        '<div class="rounded-circle bg-primary d-inline-flex justify-content-center align-items-center" '
        'style="width: {}px; height: {}px;">'
        '<span class="text-white" style="font-size: {}px;">{}</span>'
        '</div>',
        size, size, font_size, user.username[0].upper() if user.username else '?'
    )
