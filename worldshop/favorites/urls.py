from django.urls import path, include
from .views import add_to_favorites, remove_from_favorites, favorite_api, favorite_list

app_name = 'favorites'

urlpatterns = [
    path('favorites/', include([
        path('', favorite_list, name='list'),
        path('add/', add_to_favorites, name='add'),
        path('remove/', remove_from_favorites, name='remove'),
        path('api/', favorite_api, name='api')
    ])),
]
