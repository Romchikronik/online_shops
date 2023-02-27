from django.urls import path, re_path     # Импортируем path
from django.views.decorators.csrf import csrf_exempt

from .views import *             # Импортируем наши представления

urlpatterns = [
    path('', WorldStoreOnlineShopList.as_view(), name='index'),
    path('login_registration/', login_registration, name='login_registration'),

    path('telegram-auth-callback/', telegram_auth_callback, name='telegram-auth-callback'),

    # re_path(r"^account/login/$", LoginView.as_view(), name="account_login"),
    # re_path(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    # re_path(r"^account/", include("account.urls")),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # path('telegram-auth/', TelegramAuthView.as_view(), name='telegram-auth'),
    # path('telegram-auth-callback/', TelegramAuthCallbackView.as_view(), name='telegram-auth-callback'),


    re_path(r'^api/online_shop/(?P<pk>\d+)/like/$',
            csrf_exempt(VotesView.as_view(model=OnlineShop, vote_type=LikeDislike.LIKE)),
            name='online_shop_like'),
    re_path(r'^api/online_shop/(?P<pk>\d+)/dislike/$',
            csrf_exempt(VotesView.as_view(model=OnlineShop, vote_type=LikeDislike.DISLIKE)),
            name='online_shop_dislike'),

    # re_path(r'^api/online_shop/(?P<pk>\d+)/bookmark/$', BookmarkView.as_view(model=BookmarkOnlineshop),
    #         name='onlineshop_bookmark'),
    path('favorites/', productFavorites, name="bookmarks"),

    path('category/<slug:category_slug>/', OnlineShopByCategory.as_view(), name='online_shop_by_category'),


    re_path(r'(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/product/delete/(?P<product_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/',
            ProductDelete.as_view(), name='delete_product'),

    # DELETE ONLINESHOP
    re_path('online_shop/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/delete',
            OnlineShopDelete.as_view(), name='delete_onlineshop'),


    # re_path(r'save_description/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/', save_content, name='create_description'),(?P<pk>[0-9]+)


    re_path(r'online_shop/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/save_description/', save_content,
            name='save_description'),
    re_path(r'online_shop/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/edit_description/', ContentEdit.as_view(),
            name='edit_description'),  # <int:content_pk>

    re_path(r'online_shop/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/save_geo/', save_geo,
            name='save_geo'),

    re_path(r'online_shop/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/edit_geo/', GeoEdit.as_view(),
            name='edit_geo'), # <int:geo_pk>

    path('search/', ESearchView.as_view(), name='search'),
    path('category/<slug:category_slug>/search_by_online_shops/', CatESearchView.as_view(), name='search_by_online_shops'),
    path('search_by_products/', SearchViewByProducts.as_view(), name='search_by_products'),
    path('category/<slug:category_slug>/search_by_products/', CatSearchViewByProducts.as_view(),
         name='search_by_products_of_category'),

    re_path(r'online_shop/update/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/', OnlineShopUpdate.as_view(), name='update_profile'),
    re_path(r'online_shop/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/', OnlineShopDetail.as_view(), name='online_shop_detail'), # <int:onlineshop_pk>/

    re_path(r'(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/product/update/(?P<product_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/', edit_product, name='update_product'),
    re_path(r'(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/product/(?P<product_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/', ProductDetail.as_view(), name='product_detail'),
    re_path(r'(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/create_product/', add_product, name='create_product'),

    # path('bookmarks/', bookmarks, name="bookmarks"),
    path('create_profile/', CreateProfilePageView.as_view(), name='create_profile'),
    re_path(r'save_review/(?P<onlineshop_pk>\d+)/(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/', save_review, name='save_review'),
    #(?P<onlineshop_slug>[-a-zA-Zа-яА-ЯЁё0-9_]+)/
    # path('search/', SearchResults.as_view(), name='search_results'),
]
