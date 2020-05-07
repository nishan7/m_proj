from django import template
from mapp.models import CATEGORY_CHOICES, Assignment

register = template.Library()


# @register.filter
# def cart_item_count(user):
#     if user.is_authenticated:
#         qs = Order.objects.filter(user=user, ordered=False)
#         if qs.exists():
#             return qs[0].items.count()
#     return 0

@register.simple_tag
def get_total_price(user, object_list):
    tp =0
    for assigm in object_list:
        tp += assigm.price
    print(tp)
    return tp


@register.simple_tag
def get_category_tuples():
    return CATEGORY_CHOICES

@register.simple_tag
def is_booked(user, adv, handyman):
    if user.is_authenticated:
        qs = Assignment.objects.filter(client=user, advertisment_id=adv, handyman=handyman)
        if qs.exists():
            return True
    return False

from unidecode import unidecode
from django.template.defaultfilters import slugify

def slug(value):
    return slugify(unidecode(value))

register.filter('slug', slug)