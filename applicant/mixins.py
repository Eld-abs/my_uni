from django.shortcuts import get_object_or_404
from main.models import Profile


# находим пользователя когда оно авторизовано
class ProfileMixins:
  def get_profile(self):
    user = self.request.user
    return get_object_or_404(Profile, user=user)