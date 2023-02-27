from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum, Q
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator

# phone_validator = RegexValidator(r"^\+\d{12}$", "The phone number provided is invalid")


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     # phone = models.CharField(max_length=200, validators=[phone_validator], unique=True)
#
#     REQUIRED_FIELDS = ["email"]


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def online_shops(self):
        return self.get_queryset().filter(content_type__model='onlineshop')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # default=0
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Region(models.Model):
    region = models.CharField(max_length=100, verbose_name='Регион')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.region

    def get_absolute_url(self):
        return reverse('region', kwargs={'region_slug': self.slug})

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='worldstore_categories/', verbose_name='Изображение')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Category slug = {self.slug}, title = {self.title}'

    @property  # Получение
    def get_image_url(self):
        try:
            url = self.image.url
        except:
            url = 'https://275506.selcdn.ru/digital/10/object/1226999/L1hf69dD2Av0.peg'
        return url

    def get_absolute_url(self):
        return reverse('online_shop_by_category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class OnlineShopManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(category__title__icontains=query)
                         | Q(region__region__icontains=query) | Q(product__title__icontains=query)
                         | Q(product__desc__icontains=query) | Q(content__content__icontains=query))
            qs = qs.filter(or_lookup).distinct()

        return qs


class OnlineShop(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='online_shops')
    title = models.CharField(max_length=24, verbose_name='Название магазина')
    slug = models.SlugField(max_length=30, db_index=True, verbose_name='URL', allow_unicode=True)     #unique=True
    phone_number = models.IntegerField(verbose_name='Телефон') # узб номер 13 символов хватит он должен быть уникальным?
    photo = models.ImageField(upload_to='profile_photos/%Y/%m/%d/', null=True, blank=True, verbose_name='Фото профиля')
    bg = models.ImageField(upload_to='bg_photos/%Y/%m/%d/', null=True, blank=True, verbose_name='Задний фон')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Активировано')
    tg = models.URLField(null=True, blank=True, verbose_name='Телеграм')
    insta = models.URLField(null=True, blank=True, verbose_name='Инстаграм')

    is_top = models.BooleanField(default=False, verbose_name='В топе')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name='Регион')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = OnlineShopManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return f'OnlineShop slug = {self.slug}, title = {self.title}'

    def get_absolute_url(self):
        # unique_shop_slug = self.slug + str(self.user.primary_key)
        return reverse('online_shop_detail', kwargs={'onlineshop_slug': self.slug, 'onlineshop_pk': self.pk})  #+ str(self.user)  str(self.user.primary_key)

    @property  # Получение
    def get_image_url(self):
        try:
            url = self.photo.url
        except:
            url = 'https://275506.selcdn.ru/digital/10/object/1226999/L1hf69dD2Av0.peg'
        return url

    @property  # Получение
    def get_bg_url(self):
        try:
            url = self.bg.url
        except:
            url = 'https://funart.pro/uploads/posts/2021-04/1618513443_23-funart_pro-p-oboi-fon-fon-goluboi-gradient-24.png'
        return url

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Онлайн магазин'
        verbose_name_plural = 'Онлайн магазины'
        ordering = ['-time_update']


# class ContentManager(models.Manager):
#     use_for_related_fields = True
#
#     def search(self, query=None):
#         qs = self.get_queryset()
#         if query:
#             or_lookup = (Q(content__icontains=query))
#             qs = qs.filter(or_lookup).distinct()
#
#         return qs


class Content(models.Model):
    online_shop = models.OneToOneField(OnlineShop, on_delete=models.CASCADE, verbose_name='Магазин')
    content = models.TextField(max_length=5000, blank=True, verbose_name='Описание магазина')
    # time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # objects = ContentManager()


class Geo(models.Model):
    online_shop = models.OneToOneField(OnlineShop, on_delete=models.CASCADE, verbose_name='Магазин')
    geo = models.URLField(blank=True, null=True, verbose_name='Геолокация')


class ProductManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(desc__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class Product(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название товара')
    slug = models.SlugField(max_length=30, db_index=True, verbose_name='URL', allow_unicode=True)
    discount = models.BooleanField(default=False, verbose_name='Акция')
    quantity = models.CharField(max_length=50, null=True, blank=True, verbose_name='Количество')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')   # CharField сделать
    desc = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    phone_number = models.IntegerField(verbose_name='Телефон')  # изменить количесвто мах символов
    # не знаю сработает или нет если что буду использовать данную функцию в views.py
    deliver = models.CharField(max_length=60, verbose_name='Доставка')
    is_published = models.BooleanField(default=True, verbose_name='Активировано')

    online_shop = models.ForeignKey(OnlineShop, on_delete=models.CASCADE, verbose_name='Магазин')
    objects = ProductManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return f'Product slug = {self.slug}, title = {self.title}'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'onlineshop_pk': self.online_shop.pk, 'onlineshop_slug': self.online_shop.slug, 'product_slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


def get_image_filename(instance, filename):
    slug = instance.product.slug
    return "product_images/%s-%s" % (slug, filename)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    images = models.ImageField(upload_to=get_image_filename, null=True, blank=True, verbose_name='Image')

    @property  # Получение
    def get_image_url(self):
        try:
            url = self.images.url
        except:
            url = 'https://wordassociations.net/image/200x/svg_to_png/Anonymous_aiga_information_.png'
        return url

    # def __str__(self):
    #     return self.product


class Review(models.Model):
    text = models.TextField(max_length=255, verbose_name='Отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    online_shop = models.ForeignKey(OnlineShop, on_delete=models.CASCADE, verbose_name='Магазин')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикования')

    def save(self, *args, **kwargs):
        unique = self.__class__.objects.filter(author=self.author, online_shop=self.online_shop)
        if unique.exists():
            self.id = unique[0].id
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # unique_together = ('author', 'online_shop')

# @receiver(post_delete, sender=OnlineShop)
# def photo_post_delete_handler(sender, **kwargs):
#     photo = kwargs['instance']
#     storage, path = photo.photo.storage, photo.photo.path
#     storage.delete(path)
