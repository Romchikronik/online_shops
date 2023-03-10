# Generated by Django 4.1.3 on 2023-03-03 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import worldstore.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='Название')),
                ('title_uz', models.CharField(max_length=50, null=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('image', models.ImageField(upload_to='worldstore_categories/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='OnlineShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=24, verbose_name='Название магазина')),
                ('slug', models.SlugField(allow_unicode=True, max_length=30, verbose_name='URL')),
                ('phone_number', models.IntegerField(verbose_name='Телефон')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/%Y/%m/%d/', verbose_name='Фото профиля')),
                ('bg', models.ImageField(blank=True, null=True, upload_to='bg_photos/%Y/%m/%d/', verbose_name='Задний фон')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Активировано')),
                ('tg', models.URLField(blank=True, null=True, verbose_name='Телеграм')),
                ('insta', models.URLField(blank=True, null=True, verbose_name='Инстаграм')),
                ('is_top', models.BooleanField(default=False, verbose_name='В топе')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worldstore.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Онлайн магазин',
                'verbose_name_plural': 'Онлайн магазины',
                'ordering': ['-time_update'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Название товара')),
                ('slug', models.SlugField(allow_unicode=True, max_length=30, verbose_name='URL')),
                ('discount', models.BooleanField(default=False, verbose_name='Акция')),
                ('quantity', models.CharField(blank=True, max_length=50, null=True, verbose_name='Количество')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Цена')),
                ('desc', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('phone_number', models.IntegerField(verbose_name='Телефон')),
                ('deliver', models.CharField(max_length=60, verbose_name='Доставка')),
                ('is_published', models.BooleanField(default=True, verbose_name='Активировано')),
                ('online_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldstore.onlineshop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=100, verbose_name='Регион')),
                ('region_ru', models.CharField(max_length=100, null=True, verbose_name='Регион')),
                ('region_uz', models.CharField(max_length=100, null=True, verbose_name='Регион')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=255, verbose_name='Отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикования')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('online_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldstore.onlineshop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to=worldstore.models.get_image_filename, verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldstore.product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='onlineshop',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worldstore.region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='onlineshop',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.SmallIntegerField(choices=[(-1, 'Не нравится'), (1, 'Нравится')], verbose_name='Голос')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Geo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo', models.URLField(blank=True, null=True, verbose_name='Геолокация')),
                ('online_shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='worldstore.onlineshop', verbose_name='Магазин')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=5000, verbose_name='Описание магазина')),
                ('online_shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='worldstore.onlineshop', verbose_name='Магазин')),
            ],
        ),
    ]
