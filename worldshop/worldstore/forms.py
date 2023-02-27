from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = OnlineShop
        fields = ('title',
                  'photo',
                  'bg',
                  'category',
                  'region',
                  'phone_number',
                  'tg',
                  'insta')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'header-info__input',
                'placeholder': _('Название магазина')
            }),
            'photo': forms.FileInput(attrs={
                'id': 'profile_image',
                'class': 'prof_photo'
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'header-info__input',
                'placeholder': _('Номер телефона')
            }),
            'tg': forms.URLInput(attrs={
                'class': 'header-info__input',
                'placeholder': _('Ссылка на аккаунт telegram')
            }),
            'insta': forms.URLInput(attrs={
                'class': 'header-info__input',
                'placeholder': _('Ссылка на аккаунт instagram')
            }),
            'category': forms.Select(attrs={
                'class': 'header-info__select-cat',
            }),
            'region': forms.Select(attrs={
                'class': 'header-info__select-cat',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = _('Категория не выбрана')
        self.fields['region'].empty_label = _('Регион не выбран')

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 24:
    #         raise ValidationError('Длина названия недолжна превышать 24 символа')
    #
    #     return title

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(str(phone_number)) > 12:
            raise ValidationError(_('Длина телефона превышает 12 символов'))

        return phone_number

    def clean_tg(self):
        tg = self.cleaned_data['tg']
        if tg is None:
            pass
        elif not 't.me' in tg:
            raise ValidationError(_('Введите корректную ссылку на telegram профиль'))

        return tg

    def clean_insta(self):
        insta = self.cleaned_data['insta']
        if insta is None:
            pass
        elif not 'instagram' in insta:
            raise ValidationError(_('Введите корректную ссылку на instagram профиль'))

        return insta

    def handler_view(self, request):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid(): form.save()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'desc',
            'phone_number',
            'deliver',
        )

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'product-form__field',
                'placeholder': _('Название')
            }),
            # 'discount': forms.CheckboxInput(),
            # 'quantity': forms.TextInput(attrs={
            #     'class': 'product-form__field',
            #     'placeholder': 'В наличии'
            # }),
            'price': forms.NumberInput(attrs={
                'class': 'product-form__field',
                'placeholder': _('Цена (сум)')
            }),
            'desc': forms.Textarea(attrs={
                'class': 'product-form__field',
                'placeholder': _('Описание'),
                'style': 'resize: none;'
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'product-form__field',
                'placeholder': _('Номер телефона')
            }),
            'deliver': forms.TextInput(attrs={
                'class': 'product-form__field',
                'placeholder': _('пример: Яндекс доставка')
            })
        }

    # validators = ['clean_phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(str(phone_number)) > 12:
            raise ValidationError(_('Длина телефона превышает 12 символов'))

        return phone_number


class ProductFullForm(ProductForm): #extending form

    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields + ('images',)

    images = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'multiple': True,
        'name': 'images',
        'id': 'fileMulti',
        'class': 'product_image',
        'accept': 'image'
         }))

    def __init__(self, *args, **kwargs):
        super(ProductFullForm, self).__init__(*args, **kwargs)
        self.fields['images'].required = False


class ProfileContentForm(forms.ModelForm):
    class Meta:
        model = Content

        fields = ('content',)  # online_shop

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'about__textarea',
                'placeholder': _('Введите информацию о своем магазине'),
                'name': 'content'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Это поле пустое!')
        return content

    def handler_view(self, request):
        form = ProfileContentForm(request.POST)
        if form.is_valid(): form.save()


class ProfileGeoForm(forms.ModelForm):
    class Meta:
        model = Geo

        fields = ('geo',)  # online_shop

        widgets = {
            'geo': forms.URLInput(attrs={
                'class': 'geo__field',
                'placeholder': _('Вставьте ссылку геолокации'),
                'name': 'geo'
            }),
        }

    def clean_geo(self):
        geo = self.cleaned_data.get('geo')
        if not geo:
            raise forms.ValidationError('Это поле пустое!')
        return geo

    def handler_view(self, request):
        form = ProfileContentForm(request.POST)
        if form.is_valid(): form.save()


# class ReviewForm(forms.ModelForm):
#
#     class Meta:
#         model = Review
#         fields = ('text', 'online_shop')
#
#         widgets = {
#             'text': forms.Textarea(attrs={
#                 'class': 'review-form__textarea',
#                 'placeholder': 'Введите текст'
#             }),
#             'online_shop': forms.Select(attrs={
#                 'hidden': True
#             }),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['online_shop'].empty_label = [
#             i for i in self.fields['online_shop'].choices.queryset.filter(slug__in=[OnlineShop.slug])
#         ]

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'review-form__textarea',
                'placeholder': _('Введите текст')
            })
        }




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-registration__field',
        'placeholder': _('Ваш email')
    }))

    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={   # required=False,
                                'class': 'login-registration__field',
                                'placeholder': _('Пароль')
    }))


class RegistrationForm(UserCreationForm):       # Содержит в себе поля пароля и его подтверждения
    password1 = forms.CharField(
        label='Введите пароль', widget=forms.PasswordInput(attrs={  # required=False,
            'class': 'login-registration__field',
            'placeholder': _('Пароль')
        })
    )

    password2 = forms.CharField(
        label='Подтвердите пароль', widget=forms.PasswordInput(attrs={  # required=False,
            'class': 'login-registration__field',
            'placeholder': _('Подтвердите пароль')
        })
    )

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.EmailInput(attrs={
                'class': 'login-registration__field',
                'placeholder': _('Ваш email')
            })
        }

#
# from allauth.account.forms import SignupForm, LoginForm
# from django.contrib.auth import get_user_model
#
#
# class CustomSignupForm(SignupForm):
#     UserModel = get_user_model()
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if self.cleaned_data.get('pk'):
#             if self.instance.email == email:
#                 return email
#         if self.UserModel.objects.filter(email=email).exists():
#             raise forms.ValidationError('This email is already in use.')
#         return email
#
#
# class CustomLoginForm(LoginForm):
#     UserModel = get_user_model()
#     def __init__(self, *args, **kwargs):
#         super(CustomLoginForm, self).__init__(*args, **kwargs)
#         self.fields['login'].widget.attrs['placeholder'] = 'Email'
#
#     def clean_login(self):
#         email = self.cleaned_data['login']
#         if self.UserModel.objects.filter(email=email).exists():
#             return email
#         raise forms.ValidationError('This email is not registered.')

#
# from allauth.socialaccount.providers.base import ProviderAccount
# from allauth.socialaccount.providers.telegram.provider import TelegramProvider
#
#
# class CustomTelegramAccount(ProviderAccount):
#     def to_str(self):
#         return self.account.extra_data.get('first_name')
#
#
# class CustomTelegramProvider(TelegramProvider):
#     id = 'telegram_custom'
#     name = 'Telegram'
#     account_class = CustomTelegramAccount
#
#     def extract_common_fields(self, data):
#         return dict(
#             email=data.get('auth_date') + '@telegram.com',
#             username=data.get('username'),
#             first_name=data.get('first_name', ''),
#             last_name=data.get('last_name', ''),
#         )
#
#     def extract_uid(self, data):
#         return str(data.get('id'))
#
#     def get_default_scope(self):
#         return ['basic']

# import account.forms
#
#
# class SignupForm(account.forms.SignupForm):
#
#     def __init__(self, *args, **kwargs):
#         super(SignupForm, self).__init__(*args, **kwargs)
#         del self.fields["username"]
