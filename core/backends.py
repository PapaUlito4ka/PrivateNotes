from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

from core.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            print(user.password, password)
            print(user.check_password(password), self.user_can_authenticate(user))
            if user.check_password(password) and self.user_can_authenticate(user):
                print('14', user)
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
            print('20', user)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None