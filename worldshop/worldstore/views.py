import json
from random import randint
from statistics import mean

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count, Q, Min, Max, Avg
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain

from .filters import OnlineShopFilter, ProductFilter
from .forms import *

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView
from .models import *
from django.utils.translation import gettext as _

import qrcode
from PIL import Image

from django.conf import settings
from django.http import HttpResponse, Http404
import os


from telegram import Bot
from django.shortcuts import redirect, reverse
from django.conf import settings

# import telegram

import urllib.parse

import json
import requests





def telegram_auth(request):
    # Construct the authentication URL
    client_id = settings.TELEGRAM_API_ID
    redirect_uri = 'https://127.0.0.1:8000/telegram-auth-callback'
    scope = 'user:read'
    telegram_auth_url = f'https://telegram.org/auth?bot_id={client_id}&origin={urllib.parse.quote(redirect_uri)}&scope={scope}'

    # Redirect the user to the authentication URL
    return redirect(telegram_auth_url)


def telegram_auth_callback(request):
    # Retrieve the authorization code from the URL parameters
    code = request.GET.get('code')

    # Exchange the authorization code for an access token
    client_id = settings.TELEGRAM_API_ID
    client_secret = settings.TELEGRAM_API_HASH
    redirect_uri = 'https://127.0.0.1:8000/telegram-auth-callback'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getToken', data=payload)
    access_token = json.loads(response.text).get('access_token')  # settings.TELEGRAM_BOT_TOKEN

    print(response)

    # Retrieve the user's profile information
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getMe', headers=headers)
    profile = json.loads(response.text)
    print(profile)
    # Verify the user's credentials and log them in
    # password = profile['result']['id']

    if profile['result']['username'] == None:
        messages.error(request, _("Создайте username в своем телеграмм аккаунте"))
        return redirect('login_registration')
    else:
        username = profile['result']['username']   # telegram_id
        first_name = profile['result']['first_name']

    # Implement your custom authentication backend logic here
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Create a new user with the telegram_id as their username
        user = User.objects.create_user(username=username)
        user.first_name = first_name
        user.save()

    login(request, user, backend='worldshop.auth_backends.TelegramBackend')

    return redirect('/')


# def download_qr(request, qr_filename):
#     # Define the full file path
#     file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
#
#     # Check if the file exists
#     if os.path.exists(file_path):
#         # Open the file for reading
#         with open(file_path, 'rb') as f:
#             # Generate the response
#             response = HttpResponse(f.read(), content_type="image/png")
#             response['Content-Disposition'] = 'attachment; filename=' + qr_filename
#             return response
#     else:
#         # Raise a 404 error if the file does not exist
#         raise Http404

# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from .token import account_activation_token
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage


def generate_qr_code(url, title):
    # Create a QR code instance
    qr = qrcode.QRCode(version=1, box_size=9, border=3)
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    filename = f"qrcode_{title}.png"
    img.save(f'media/qr_codes/{filename}')

    return filename


class WorldStoreOnlineShopList(ListView):
    model = OnlineShop
    # template_name = 'index.html'
    template_name = 'worldstore/top_shops.html'
    context_object_name = 'online_shops'
    extra_context = {
        'title': 'World of shops'
    }


    # def get_queryset(self):
    #     return OnlineShop.objects.annotate(Count('product')).filter(is_published=True, is_top=True).select_related(
    #         'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        online_shops = OnlineShop.objects.annotate(Count('product')).filter(is_published=True, is_top=True).select_related('category')

        products = Product.objects.filter(is_published=True).order_by('-time_update')

        onlineShopsFilter = OnlineShopFilter(self.request.GET, queryset=online_shops)

        productFilter = ProductFilter(self.request.GET, queryset=products)
        products = productFilter.qs
        context['productFilter'] = productFilter
        context['products'] = products

        online_shops = onlineShopsFilter.qs
        context['onlineShopsFilter'] = onlineShopsFilter
        context['online_shops'] = online_shops
        return context


class OnlineShopByCategory(WorldStoreOnlineShopList):
    paginate_by = 24
    template_name = 'worldstore/onlineshop_by_category.html'
    slug_url_kwarg = 'category_slug'

    # def get_queryset(self):
    #
    #
    #     # sort_field = self.request.GET.get('sort')
    #     #
    #     # if sort_field:
    #     #     for online_shop in online_shops:
    #     #         products = online_shops.order_by(sort_field)
    #
    #     return online_shops

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()  # Забираем весь контекст котрый был
        category = Category.objects.get(slug=self.kwargs['category_slug'])

        online_shops = OnlineShop.objects.annotate(Count('product')).filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True
        ).order_by('-time_update').select_related('category')

        onlineShopsFilter = OnlineShopFilter(self.request.GET, queryset=online_shops)
        online_shops = onlineShopsFilter.qs
        context['onlineShopsFilter'] = onlineShopsFilter

        products = Product.objects.filter(online_shop__category__slug=self.kwargs['category_slug'], is_published=True).order_by('-time_update')
        productFilter = ProductFilter(self.request.GET, queryset=products)
        products = productFilter.qs
        context['productFilter'] = productFilter
        context['products'] = products

        # min_price = Product.objects.aggregate(Min('price'))
        # max_price = Product.objects.aggregate(Max('price'))
        # min_price = 0
        # max_price = 100000000000
        # value = Product.objects.filter(price__range=(min_price, max_price))

        # user = auth.get_user(self.request)

        # context['value'] = value
        # context['max_price'] = max_price
        # context['min_price'] = min_price

        cat_slug = category.slug
        context['cat_slug'] = cat_slug
        context['online_shops'] = online_shops
        context['title'] = _(f'Категория: {category.title}')
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            super().dispatch(request, *args, **kwargs)
        except Http404:  # Импортируем
            return redirect('index')  # Импортируем

        return super().dispatch(request, *args, **kwargs)


# class OnlineShopByRegion(WorldStoreOnlineShopList):
#     slug_url_kwarg = 'region_slug'
#
#     def get_queryset(self):
#         return OnlineShop.objects.annotate(Count('product')).filter(
#             region__slug=self.kwargs['region_slug'],
#             is_published=True,
#             is_top=True
#         ).select_related('category')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()  # Забираем весь контекст котрый был
#         region = Region.objects.get(slug=self.kwargs['region_slug'])
#
#         reg_slug = region.slug
#         context['reg_slug'] = reg_slug
#
#         context['title'] = _(f'Регион: {region.region}')
#         return context
#
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             super().dispatch(request, *args, **kwargs)
#         except Http404:  # Импортируем
#             return redirect('index')  # Импортируем
#
#         return super().dispatch(request, *args, **kwargs)
#
#
# class OnlineShopByRegionInCategories(OnlineShopByCategory, OnlineShopByRegion):
#     template_name = 'worldstore/onlineshop_by_region_&_category.html'
#
#     # def get_queryset(self):
#     #     online_shops = OnlineShop.objects.annotate(Count('product')).filter(
#     #         category__slug=self.kwargs['category_slug'],
#     #         region__slug=self.kwargs['region_slug'],
#     #         is_published=True
#     #     ).order_by('title').select_related('category')
#     #
#     #
#     #     # online_shops = online_shops.order_by('title')
#     #
#     #     return online_shops
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()  # Забираем весь контекст котрый был
#         # region = Region.objects.get(slug=self.kwargs['region_slug'])
#         # category = Category.objects.get(slug=self.kwargs['category_slug'])
#         online_shops = OnlineShop.objects.annotate(Count('product')).filter(
#             category__slug=self.kwargs['category_slug'],
#             region__slug=self.kwargs['region_slug'],
#             is_published=True
#         ).order_by('title').select_related('category')
#
#         # reg_slug = region.slug
#         # cat_slug = category.slug
#         # context['reg_slug'] = reg_slug
#         # context['cat_slug'] = cat_slug
#         # context['title'] = f'Категория: {category.title} | Регион: {region.region}'
#         context['online_shops'] = online_shops
#
#         return context
#
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             super().dispatch(request, *args, **kwargs)
#         except Http404:  # Импортируем
#             return redirect('index')  # Импортируем
#
#         return super().dispatch(request, *args, **kwargs)


class OnlineShopDetail(DetailView, MultipleObjectMixin):
    model = OnlineShop
    template_name = 'worldstore/online_shop_detail.html'
    slug_url_kwarg = 'onlineshop_slug'    # + str(User.pk)

    pk_url_kwarg = 'onlineshop_pk'
    query_pk_and_slug = True

    context_object_name = 'online_shop'

    def get_paginate_by(self, queryset):
        try:
            if self.request.user.is_authenticated and self.request.user.onlineshop.slug == self.kwargs['onlineshop_slug']:
                self.paginate_by = None
            else:
                self.paginate_by = 4
            return self.paginate_by
        except:
            self.paginate_by = 4
            return self.paginate_by

    # def get_queryset(self):
    #     return OnlineShop.objects.filter(slug=self.kwargs['onlineshop_slug'], is_published=True).select_related('category')

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(online_shop=self.get_object(), is_published=True).order_by('-time_update')
        context = super(OnlineShopDetail, self).get_context_data(object_list=products, **kwargs)

        online_shop = OnlineShop.objects.annotate(Count('review')).get(slug=self.kwargs['onlineshop_slug'],
                                                                       is_published=True, pk=self.kwargs['onlineshop_pk'])
        # try:
        #     print('Я лучше')
        #     online_shop = OnlineShop.objects.annotate(Count('review')).get(slug=self.kwargs['onlineshop_slug'],
        #                                                                is_published=True)
        # except MultipleObjectsReturned:
        #     print("Я здесь")
        #     online_shop = OnlineShop.objects.annotate(Count('review')).filter(slug=self.kwargs['onlineshop_slug'],
        #                                                                is_published=True, pk=OnlineShop.pk)

        # products = Product.objects.filter(online_shop=online_shop.pk, is_published=True) .first()

        # online_shops = OnlineShop.objects.annotate(Count('review'))

        context['reviews'] = Review.objects.order_by('-created_at').filter(online_shop__slug=online_shop.slug)
        # online_shops = OnlineShop.objects.annotate(Count('review'))
        #      return online_shops
        # можно добавить срез [:10]
        # Создать еще один context с отзывами cо срезом после 10 либо сделать условие и выводить только те
        # при нажатии на кнопку все комментарии, чтобы отражались все остальные можно через js сделать
        try:
            geo = Geo.objects.get(online_shop__slug=online_shop.slug)
            context['geo'] = geo
            context['geo_form'] = ProfileGeoForm(instance=geo)
        except:
            context['geo'] = None
            context['geo_form'] = ProfileGeoForm()

        try:
            content = Content.objects.get(online_shop__slug=online_shop.slug)
            context['content'] = content
            context['content_form'] = ProfileContentForm(instance=content)
        except:
            context['content'] = None
            context['content_form'] = ProfileContentForm()
        # context['online_shop_slug'] = online_shop.slug
        # context['online_shop'] = online_shop

        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        # На хостинге поменять
        qrcode_url = generate_qr_code(f"http://127.0.0.1:8000/online_shop/{online_shop.pk}/{online_shop.slug}/", online_shop.slug)

        context['qrcode_url'] = qrcode_url

        context['online_shop'] = online_shop
        context['products'] = products
        context['title'] = f'Магазин: {online_shop.title}'
        return context


class OnlineShopDelete(DeleteView):
    model = OnlineShop
    slug_url_kwarg = 'onlineshop_slug'
    pk_url_kwarg = 'onlineshop_pk'
    query_pk_and_slug = True
    context_object_name = 'online_shop'

    def post(self, request, *args, **kwargs):
        self.object = OnlineShop.objects.get(pk=self.kwargs['onlineshop_pk'], slug=self.kwargs['onlineshop_slug'])
        form = self.get_form()
        # response = self.process_response(request, response)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index')



class ProductDetail(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'worldstore/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(online_shop__pk=self.kwargs['onlineshop_pk'], online_shop__slug=self.kwargs['onlineshop_slug'],
                                      slug=self.kwargs['product_slug'])

        images_ids = []
        product_images = product.productimages_set.all()
        images_length = len(product_images)
        for image in range(0, images_length):
            image_idx = image
            images_ids.append(image_idx)

        similar_shops = OnlineShop.objects.annotate(Count('product')).filter(
            is_published=True, category=product.online_shop.category).exclude(title=product.online_shop.title)[
                        :30].select_related('category')

        data = []
        for i in range(32):
            if len(similar_shops) != 0:
                random_index = randint(0, len(similar_shops) - 1)
                online_shop = similar_shops[random_index]
                if online_shop not in data:
                    data.append(online_shop)

        products = Product.objects.filter(
            is_published=True, online_shop=product.online_shop).exclude(title=product.title).select_related(
            'online_shop')

        context = {'product': product,
                   'product_images': product_images,
                   'images_length': images_length,
                   'images_ids': images_ids,
                   'similar_shops': data,
                   'products': products,
                   'title': _(f'Продукт: {product.title}')}

        return self.render_to_response(context)
        # try:
        #     self.object = self.get_object()
        #     context = self.get_context_data(object=self.object)
        #     return self.render_to_response(context)
        # except MultipleObjectsReturned:

    # def get_queryset(self):
    #     return Product.objects.get(slug=self.kwargs['product_slug'], is_published=True).select_related('online_shop')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     product = Product.objects.get(online_shop__slug=self.kwargs['onlineshop_slug'], slug=self.kwargs['product_slug'])
    #
    #     images_ids = []
    #     product_images = product.productimages_set.all()
    #     images_length = len(product_images)
    #     for image in range(0, images_length):
    #         image_idx = image
    #         images_ids.append(image_idx)
    #
    #     similar_shops = OnlineShop.objects.annotate(Count('product')).filter(
    #         is_published=True, category=product.online_shop.category).exclude(title=product.online_shop.title)[:30].select_related('category')
    #
    #     products = Product.objects.filter(
    #         is_published=True, online_shop=product.online_shop).exclude(title=product.title).select_related('online_shop')
    #
    #     context['products'] = products
    #     context['similar_shops'] = similar_shops
    #     context['product_images'] = product_images
    #     context['images_length'] = images_length
    #     context['images_ids'] = images_ids
    #
    #     context['title'] = f'Продукт: {product.title}'
    #     return context


class CreateProfilePageView(LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    template_name = 'worldstore/new_profile.html'
    extra_context = {
        'title': _('Создание магазина')
    }

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            'user': user.username
        })

        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OnlineShopUpdate(UpdateView):
    model = OnlineShop
    form_class = ProfileForm
    slug_url_kwarg = 'onlineshop_slug'
    pk_url_kwarg = 'onlineshop_pk'
    query_pk_and_slug = True
    template_name = 'worldstore/new_profile.html'

    extra_context = {
        'title': _('Обновление магазина')
    }


def add_product(request,  onlineshop_pk, onlineshop_slug,):
    online_shop = OnlineShop.objects.get(slug=onlineshop_slug, pk=onlineshop_pk)
    products = Product.objects.filter(online_shop=online_shop)
    data = []
    for product in products:
        data.append(product.title)

    if request.method == "POST":
        form = ProductFullForm(request.POST, request.FILES)  # initial={'online_shop': online_shop.title}
        files = request.FILES.getlist('images')
        if form.is_valid():
            title = form.cleaned_data['title']
            # discount = form.cleaned_data['discount']
            # quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            desc = form.cleaned_data['desc']
            phone_number = form.cleaned_data['phone_number']
            deliver = form.cleaned_data['deliver']
            online_shop = online_shop

            if not title in data:
                if len(files) <= 5:
                    product_obj = Product.objects.create(
                        title=title,
                        # discount=discount,
                        # quantity=quantity,
                        price=price,
                        desc=desc,
                        phone_number=phone_number,
                        deliver=deliver,
                        online_shop=online_shop
                    )

                    for f in files:
                        ProductImages.objects.create(product=product_obj, images=f)
                    return redirect('online_shop_detail', onlineshop_pk, onlineshop_slug)
                else:
                    messages.error(request, _(f'Вы можете загружать до 5 картинок, загрузите меньше картинок'))
                    return redirect('create_product', onlineshop_pk, onlineshop_slug)
            else:
                messages.error(request,
                               _(f'Товар с названием {title} уже существует в вашем магазине. Используйте другое название'))

                return redirect('create_product', onlineshop_pk, onlineshop_slug)
    else:
        form = ProductFullForm()
        # print("Form invalid")

    context = {
        'form': form,
        'title': _('Создание продукта')
    }

    return render(request, 'worldstore/new_product.html', context)


def edit_product(request, onlineshop_pk, onlineshop_slug, product_slug):
    online_shop = OnlineShop.objects.get(pk=onlineshop_pk, slug=onlineshop_slug)
    product = Product.objects.get(online_shop__pk=onlineshop_pk, online_shop__slug=onlineshop_slug, slug=product_slug)

    products = Product.objects.filter(online_shop=online_shop)
    data = []
    for p in products:
        if p.title != product.title:
            data.append(p.title)

    product_images = product.productimages_set.all()
    images_length = len(product_images)
    # print(product_images)

    if request.method == "POST":
        form = ProductFullForm(request.POST, request.FILES, instance=product)  # initial={'online_shop': online_shop.title}
        files = request.FILES.getlist('images')
        if form.is_valid():
            product.title = request.POST.get("title")
            # product.discount = request.POST.get("discount")
            product.quantity = request.POST.get("quantity")
            product.price = request.POST.get("price")
            product.phone_number = request.POST.get("phone_number")
            product.deliver = request.POST.get("deliver")
            product.online_shop = request.user.onlineshop
            # product.save()
            if not product.title in data:
                if len(files) <= 5:
                    if files != []:
                        product_images.delete()

                        for f in files:
                            ProductImages.objects.create(product=product, images=f)

                    product.save()
                    return redirect('product_detail', onlineshop_pk, onlineshop_slug, product.slug)
                else:
                    messages.error(request, _(f'Вы можете загружать до 5 картинок, загрузите меньше картинок'))
                    return redirect('update_product', onlineshop_pk, onlineshop_slug, product.slug)
            else:
                messages.error(request,
                               _(f'Товар с названием {product.title} уже существует в вашем магазине. Используйте другое название'))

                return redirect('update_product', onlineshop_pk, onlineshop_slug, product.slug)
    else:
        form = ProductFullForm(instance=product)
        # print("Form invalid")

    context = {
        'form': form,
        'product_images': product_images,
        'images_length': images_length,
        'title': _(f'Изменение продукта {product.title}')
    }

    return render(request, 'worldstore/new_product.html', context)


class ProductDelete(DeleteView):
    model = Product
    slug_url_kwarg = 'product_slug'
    # success_url = reverse_lazy('online_shop_detail')
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        self.object = Product.objects.get(online_shop__pk=self.kwargs['onlineshop_pk'], online_shop__slug=self.kwargs['onlineshop_slug'],
                                          slug=self.kwargs['product_slug'])
        form = self.get_form()

        # response = self.process_response(request, response)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('online_shop_detail', kwargs={'onlineshop_pk': self.kwargs['onlineshop_pk'], 'onlineshop_slug': self.kwargs['onlineshop_slug']})


def save_content(request, onlineshop_pk, onlineshop_slug):
    online_shop = OnlineShop.objects.get(pk=onlineshop_pk, slug=onlineshop_slug)
    if request.method == 'POST':
        content_form = ProfileContentForm(data=request.POST)
        if content_form.is_valid():

            try:
                content = content_form.cleaned_data['content']
                Content.objects.create(online_shop=online_shop, content=content)
                return redirect('online_shop_detail', onlineshop_pk, onlineshop_slug)
            except IntegrityError:
                messages.error(request,
                               _(f'{request.user.username}, у вас уже есть описание магазина {online_shop.title}. Но вы можете его изменить'))

    else:
        content_form = ProfileContentForm()
    return redirect('online_shop_detail', onlineshop_pk, onlineshop_slug)


class ContentEdit(UpdateView):
    model = Content
    form_class = ProfileContentForm
    # fields = ['content']

    def post(self, request, *args, **kwargs):
        self.object = Content.objects.get(online_shop__pk=self.kwargs['onlineshop_pk'], online_shop__slug=self.kwargs['onlineshop_slug'])
        content_form = self.get_form()

        # response = self.process_response(request, response)
        if content_form.is_valid():
            return self.form_valid(content_form)
        else:
            return self.form_invalid(content_form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('online_shop_detail', kwargs={'onlineshop_pk': self.kwargs['onlineshop_pk'], 'onlineshop_slug': self.kwargs['onlineshop_slug']})


def save_geo(request, onlineshop_pk, onlineshop_slug):
    online_shop = OnlineShop.objects.get(pk=onlineshop_pk, slug=onlineshop_slug)
    if request.method == 'POST':
        geo_form = ProfileGeoForm(data=request.POST)
        if geo_form.is_valid():
            geo = geo_form.cleaned_data['geo']
            Geo.objects.create(online_shop=online_shop, geo=geo)
            return redirect('online_shop_detail', onlineshop_pk, onlineshop_slug)
    else:
        geo_form = ProfileGeoForm()
    return redirect('online_shop_detail', onlineshop_pk, onlineshop_slug)


class GeoEdit(UpdateView):
    model = Geo
    form_class = ProfileGeoForm

    def post(self, request, *args, **kwargs):
        self.object = Geo.objects.get(online_shop__pk=self.kwargs['onlineshop_pk'], online_shop__slug=self.kwargs['onlineshop_slug'])
        geo_form = self.get_form()

        # response = self.process_response(request, response)
        if geo_form.is_valid():
            return self.form_valid(geo_form)
        else:
            return self.form_invalid(geo_form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('online_shop_detail', kwargs={'onlineshop_pk': self.kwargs['onlineshop_pk'], 'onlineshop_slug': self.kwargs['onlineshop_slug']})


def save_review(request, onlineshop_pk, onlineshop_slug):
    form = ReviewForm(data=request.POST)
    online_shop = OnlineShop.objects.get(pk=onlineshop_pk, slug=onlineshop_slug)
    if form.is_valid():
        try:
            review = form.save(commit=False)
            review.author = request.user
            review.online_shop = online_shop
            review.online_shop__pk = onlineshop_pk
            review.online_shop__slug = onlineshop_slug
            review.save()
        except:
            messages.error(request, _(f'Вы уже оставляли отзыв у магазина {online_shop.title}'))
    else:
        pass
        # ReviewForm()
    return redirect('online_shop_detail', onlineshop_pk, onlineshop_slug)


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


# class BookmarkView(View):
#     # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
#     model = None
#
#     # def get_client_ip(self, request):
#     #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     #     if x_forwarded_for:
#     #         ip = x_forwarded_for.split(',')[-1].strip()
#     #     else:
#     #         ip = request.META.get('REMOTE_ADDR')
#     #     return ip
#
#     def post(self, request, pk):
#         # нам потребуется пользователь
#
#         user = auth.get_user(request)
#         # пытаемся получить закладку из таблицы, или создать новую
#         bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
#         # если не была создана новая закладка,
#         # то считаем, что запрос был на удаление закладки
#         if not created:
#             bookmark.delete()
#
#         return HttpResponse(
#             json.dumps({
#                 "result": created,
#                 "count": self.model.objects.filter(obj_id=pk).count()
#             }),
#             content_type="application/json"
#         )

def productFavorites(request):
    online_shops = OnlineShop.objects.all().order_by('title')
    # req_onlineshop = request.session.get('favorites')
    user_session = request.session.get('favorites')
    # print(user_session)
    # print(online_shops)
    context = {}

    if user_session != None:
        paginator = Paginator(user_session, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    # online_shop = OnlineShop.objects.get(pk=)

        context['page_obj'] = page_obj
    context['online_shops'] = online_shops

    return render(request, 'worldstore/bookmarks.html', context)


# def bookmarks(request):
#     user = auth.get_user(request)
#     # if request.user.is_authenticated:
#     bookmark_list = user.bookmarkonlineshop_set.all()
#     paginator = Paginator(bookmark_list, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'worldstore/bookmarks.html', {'page_obj': page_obj})
        # регистрация


class ESearchView(View):
    template_name = 'worldstore/search.html'

    def get(self, request, *args, **kwargs):
        context = {}

        q = request.GET.get('q')
        if q:
            query_sets = []  # Total QuerySet

            online_shops = OnlineShop.objects.annotate(Count('product')).filter(is_published=True).select_related('category')
            # productFilter = ProductFilter(self.request.GET, queryset=products)
            onlineShopsFilter = OnlineShopFilter(self.request.GET, queryset=online_shops)
            online_shops = onlineShopsFilter.qs
            context['onlineShopsFilter'] = onlineShopsFilter
            context['online_shops'] = online_shops


            # Searching for all models
            query_sets.append(OnlineShop.objects.search(query=q))
            # query_sets.append(Product.objects.search(query=q))
            # query_sets.append(Content.objects.search(query=q))

            # and combine results
            final_set = list(chain(*query_sets))
            final_set.sort(key=lambda x: x.time_update)  # Sorting
            # seen = {}
            # new_list = [seen.setdefault(x, x) for x in list(chain(*query_sets)) if x not in seen]

            context['last_question'] = '?q=%s' % q

            current_page = Paginator(final_set, 12)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request=request, template_name=self.template_name, context=context)


class CatESearchView(ESearchView):
    template_name = 'worldstore/search_by_online_shops.html'

    def get(self, request, *args, **kwargs):
        super()
        context = {}

        q = request.GET.get('q')
        if q:
            query_sets = []  # Total QuerySet
            cat_slug = self.kwargs['category_slug']
            context['cat_slug'] = cat_slug

            # Searching for all models
            query_sets.append(OnlineShop.objects.search(query=q))
            # query_sets.append(Product.objects.search(query=q))
            # query_sets.append(Content.objects.search(query=q))

            # and combine results
            final_set = list(chain(*query_sets))
            final_set.sort(key=lambda x: x.time_update)  # Sorting
            # seen = {}
            # new_list = [seen.setdefault(x, x) for x in list(chain(*query_sets)) if x not in seen]

            context['last_question'] = '?q=%s' % q

            current_page = Paginator(final_set, 12)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request=request, template_name=self.template_name, context=context)


class SearchViewByProducts(View):
    template_name = 'worldstore/search_by_products.html'

    def get(self, request, *args, **kwargs):
        context = {}

        p = request.GET.get('p')
        if p:
            query_sets = []  # Total QuerySet

            products = Product.objects.filter(is_published=True).order_by('-time_update')
            productFilter = ProductFilter(self.request.GET, queryset=products)
            products = productFilter.qs
            context['productFilter'] = productFilter
            context['products'] = products
            # Searching for all models
            # query_sets.append(OnlineShop.objects.search(query=q))
            query_sets.append(Product.objects.search(query=p))
            # query_sets.append(Content.objects.search(query=q))

            # and combine results
            final_set = list(chain(*query_sets))
            final_set.sort(key=lambda x: x.time_update)  # Sorting
            # seen = {}
            # new_list = [seen.setdefault(x, x) for x in list(chain(*query_sets)) if x not in seen]

            context['last_question'] = '?p=%s' % p

            current_page = Paginator(final_set, 12)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request=request, template_name=self.template_name, context=context)


class CatSearchViewByProducts(SearchViewByProducts):      # OnlineShopByCategory
    template_name = 'worldstore/search_by_products_of_category.html'

    def get(self, request, *args, **kwargs):
        context = {}

        p = request.GET.get('p')

        if p:
            query_sets = []  # Total QuerySet
            cat_slug = self.kwargs['category_slug']
            context['cat_slug'] = cat_slug

            sort_field = self.request.GET.get('sort')

            if sort_field:
                products = Product.objects.filter(title=p).order_by(sort_field)
                # print(p)
                context['products'] = products
            # Searching for all models
            # query_sets.append(OnlineShop.objects.search(query=q))
            query_sets.append(Product.objects.search(query=p))
            # query_sets.append(Content.objects.search(query=q))

            # and combine results
            final_set = list(chain(*query_sets))
            final_set.sort(key=lambda x: x.time_update)  # Sorting
            # seen = {}
            # new_list = [seen.setdefault(x, x) for x in list(chain(*query_sets)) if x not in seen]

            context['last_question'] = '?p=%s' % p

            current_page = Paginator(final_set, 12)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)


        return render(request=request, template_name=self.template_name, context=context)


def login_registration(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        'title': _('Войти или зарегистрироваться')
    }

    return render(request, 'worldstore/login_registration.html', context)


def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        # messages.success(request, _('Отлично! Вы прошли регистрацию! Теперь можете авторизоваться'))
        # Авторизовываем пользователя после успешной регистрации
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(request, user)
        return render(request, 'index.html')
    else:
        messages.error(request, _('''Пароль не должен быть слишком похож на другую вашу личную информацию. \n
Ваш пароль должен содержать как минимум 8 символов.  \n
Пароль не должен быть слишком простым и распространенным. \n 
Пароль не может состоять только из цифр.'''))
        return redirect('login_registration')

#
# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             # save form in the memory not in database
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             # to get the domain of the current site
#             current_site = get_current_site(request)
#             mail_subject = 'Activation link has been sent to your email id'
#             message = render_to_string('worldstore/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#         # else:
#         #     messages.error(request, '''Пароль не должен быть слишком похож на другую вашу личную информацию.
#         # Ваш пароль должен содержать как минимум 8 символов.
#         # Пароль не должен быть слишком простым и распространенным.
#         # Пароль не может состоять только из цифр.''')
#         #     return redirect('login_registration')
#     else:
#         form = RegistrationForm()
#
#     # messages.success(request, 'Отлично! Вы прошли регисрацию! Теперь можете авторизоваться')
#     # return render(request, 'index.html')
#     # return render(request, 'worldstore/login_registration.html', {'registration_form': form})
#     return redirect('login_registration')


# def register(request):
#     form = RegistrationForm(data=request.POST)
#     if form.is_valid():
#         user = form.save()
#         messages.success(request, 'Отлично! Вы прошли регисрацию! Теперь можете авторизоваться')
#     else:
#         return messages.error(request, 'Что-то пошло не так')
#     return redirect('login_registration')


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user != None:
            login(request, user, backend='worldshop.auth_backends.TelegramBackend')  # убрать backend
            # messages.success(request, 'Отлично! Вы успешно зашли в акаунт')
            return redirect('index')
        else:
            messages.error(request, 'Что-то пошло не так')
            return redirect('login_registration')
    else:
        messages.error(request, _('Не верно имя пользователя или пароль'))
    return redirect('login_registration')


def user_logout(request):
    logout(request)
    return redirect('index')


# import worldstore.forms
# import account.forms
# import account.views


# class LoginView(account.views.LoginView):
#     form_class = account.forms.LoginEmailForm
#
#
# class SignupView(account.views.SignupView):
#
#     form_class = worldstore.forms.SignupForm
#
#     def generate_username(self, form):
#         username = form.cleaned_data["email"]
#         return username
#
#     def after_signup(self, form):
#         # do something
#         super(SignupView, self).after_signup(form)

