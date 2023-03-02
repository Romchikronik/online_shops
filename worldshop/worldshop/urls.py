"""worldshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from worldshop import settings
from django.conf.urls.static import static

from allauth.account.views import LogoutView
from allauth.socialaccount import views as social_views

# from account.views import PasswordResetTokenView

# from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r"^account/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", PasswordResetTokenView.as_view(),
    #         name="account_password_reset_token")
]

urlpatterns += i18n_patterns(                         # для мультиязычности
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('worldstore.urls')),
    path('', include('favorites.urls')),

    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/social/signup/', social_views.signup, name='socialaccount_signup'),
    # path('login/', LoginView.as_view(), name='account_login'),
    # path('logout/', LogoutView.as_view(), name='account_logout'),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
