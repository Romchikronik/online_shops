from django import template
from django.db.models import Count
from worldstore.models import Category, OnlineShop
from django.urls import translate_url as django_translate_url
from statistics import mean

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.annotate(Count('onlineshop'))
    return categories


# @register.simple_tag()
# def get_regions():
#     regions = Region.objects.annotate(Count('onlineshop'))
#     return regioncs


@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    path = context.get('request').get_full_path()
    return django_translate_url(path, lang_code)
#
# @register.simple_tag()
# def get_online_shops():
#     online_shops = OnlineShop.objects.annotate(Count('product'))
#     return online_shopz

