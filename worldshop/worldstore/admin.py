from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.auth.admin import UserAdmin
from .models import User


# class UserUsers(UserAdmin):
#     list_display = ('pk', 'username', 'email')
#     list_display_links = ('pk', 'username', 'email')
#
#
# admin.site.register(User, UserUsers)


class RegionAdmin(TranslationAdmin):
    list_display = ('pk', 'region', 'slug')
    list_display_links = ('region',)
    prepopulated_fields = {"slug": ("region",)}


class CategoryAdmin(TranslationAdmin):
    list_display = ('pk', 'title', 'slug', 'image')
    list_display_links = ('title', )
    prepopulated_fields = {"slug": ("title",)}


class OnlineShopAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_published', 'is_top')
    list_editable = ('is_published', 'is_top')
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'online_shop', 'phone_number', 'is_published')
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}


class GeoAdmin(admin.ModelAdmin):
    list_display = ('geo', 'online_shop')


class ContentAdmin(admin.ModelAdmin):
    list_display = ('cut_text', 'online_shop')

    def cut_text(self, obj):
        if len(obj.content) > 30:
            return obj.content[:30] + '...'
        else:
            return obj.content

    cut_text.short_description = 'контент'


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'images')


class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('vote', 'user')
    list_display_links = ('user',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'online_shop', 'cut_text', 'created_at')

    def cut_text(self, obj):
        if len(obj.text) > 30:
            return obj.text[:30] + '...'
        else:
            return obj.text

    cut_text.short_description = 'отзыв'


admin.site.register(OnlineShop, OnlineShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(LikeDislike, LikeDislikeAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Geo, GeoAdmin)

