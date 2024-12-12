from django.urls import path
from . import views
from django.contrib.auth.views import  LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.redirect_to_login, name='redirect-to-login'),  # Главная страница перенаправляет на регистрацию
    path('registration/', views.FirstStepRegistrationView.as_view(), name='first_step_registration'),  # Страница регистрации
    path('registration/step2/', views.SecondStepRegistrationView.as_view(), name='second_step_registration'),  # Страница регистрации шаг второй
    path('login/', views.LoginUserView.as_view(), name='login'),  # Страница входа
    path('home/', views.home, name='home'),
    path('help/', views.help, name='help'),
    path('logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)