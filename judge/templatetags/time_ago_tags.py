from datetime import datetime

from django.template import Library

register = Library()


@register.simple_tag
def time_ago(date):
    now = datetime.now()
    if date.day == now.day:
        hours = now.hour - date.hour
        if hours <= 1:
            return f'{hours} hour ago'

        return f'{hours} hours ago'
    if date.month == now.month:
        days = now.day - date.day
        if days == 1:
            return '1 day ago'
        return f'{days} ago'
    if date.year == now.year:
        months = now.month - date.month
        if months == 1:
            return '1 month ago'
        return f'{months} ago'
