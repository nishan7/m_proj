from django import template
from mapp.models import Assignment

register = template.Library()


@register.filter
def is_booked(user, adv, handyman):
    if user.is_authenticated:
        qs = Assignment.objects.filter(client=user, advertisment_id=adv, handyman=handyman)
        if qs.exists():
            return True
    return False

