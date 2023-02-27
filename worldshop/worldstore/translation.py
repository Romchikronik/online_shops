from modeltranslation.translator import register, TranslationOptions
from .models import Category, Region


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region',)
