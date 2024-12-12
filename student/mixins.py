
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin



# проверяем авторизован ли ползоваетль если нет перенаправляем login_url(LoginRequiredMixin этот класс делает это же самое и я написал собственный поскольку хотел узнать как это делается)
class ProfileRequiredMixins(LoginRequiredMixin):
  login_url = 'main:login'
  # если пользователь был перенаправлен в login и прошол авторизацию, пользователь будет возвращен в ту же страницу где оно находился до этого
  redirect_field_name = 'next'

  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect(self.get_login_url())
    return super().dispatch(request, *args, **kwargs)