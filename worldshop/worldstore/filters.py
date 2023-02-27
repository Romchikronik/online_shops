import django_filters
from django_filters import ModelChoiceFilter
from django.utils.translation import gettext_lazy as _

from .models import OnlineShop, Category, Region, Product


# class OnlineShopFilter(django_filters.FilterSet):
#     class Meta:
#         model = OnlineShop
#         fields = ['category', 'region']


class OnlineShopFilter(django_filters.FilterSet):
    class Meta:
        model = OnlineShop
        fields = ('category', 'region')

    category = ModelChoiceFilter(
        field_name="category",
        to_field_name="slug",  # slug field
        queryset=Category.objects.all(),
        empty_label=_('Категория не выбрана')
    )

    region = ModelChoiceFilter(
        field_name="region",
        to_field_name="slug",  # slug field
        queryset=Region.objects.all(),
        empty_label=_('Регион не выбран')
    )


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {'online_shop__category': ['exact'], 'online_shop__region': ['exact'], 'price': ['exact', 'gte', 'lte']}

    online_shop__category = ModelChoiceFilter(
        field_name="online_shop__category",
        to_field_name="slug",  # slug field
        queryset=Category.objects.all(),
        empty_label=_('Категория не выбрана')
    )

    online_shop__region = ModelChoiceFilter(
        field_name="online_shop__region",
        to_field_name="slug",  # slug field
        queryset=Region.objects.all(),
        empty_label=_('Регион не выбран')
    )

