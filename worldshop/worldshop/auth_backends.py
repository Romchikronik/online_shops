# from allauth.account.auth_backends import AuthenticationBackend
# from django.contrib.auth import get_user_model
#
#
# class CustomAuthenticationBackend(AuthenticationBackend):
#     def authenticate(self, request, **credentials):
#         UserModel = get_user_model()
#         email = credentials.get('email')
#         telegram_id = credentials.get('telegram_id')
#         if email:
#             try:
#                 user = UserModel.objects.get(email=email)
#             except UserModel.DoesNotExist:
#                 return None
#         elif telegram_id:
#             try:
#                 user = UserModel.objects.get(telegram_id=telegram_id)
#             except UserModel.DoesNotExist:
#                 return None
#         else:
#             return None
#         return user if self.user_can_authenticate(user) else None
#
#     def get_user(self, user_id):
#         UserModel = get_user_model()
#         try:
#             return UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class TelegramBackend(BaseBackend):
    def authenticate(self, request, username=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        return user if self.authenticate(user) else None   # authenticate

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
