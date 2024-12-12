from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm, FirstStepRegisterForm, SecondStepApplicantForm
from django.views import View
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist



def redirect_to_login(request):
  return redirect('main:login')  # Перенаправляет пользователя на страницу регистрации


def login_User(request):
  return render(request, 'main/login.html')


def home(request):
  return render(request, 'main/home.html')


def help(request):
  return render(request, 'main/help.html')


def student_home(request):
    return render(request, 'main/student_home.html')


# Первый этап регистрации
class FirstStepRegistrationView(View):
  # это отправляет пользователю html шаблон и формы(сработает до того как пользователь введёт данные)
  def get(self, request):
    # это пустые формы, сюда пользователь может ввести данные 
    form = FirstStepRegisterForm()
    # это отправляет html шаблон на страницу вмете с формай для заполнение
    return render(request, 'main/registration.html', {'form': form})
  
  # получив данные с страницы(там где формы чтобы заполнить(первого этапа)) этот метод проверит домен и решит сохранить или перенаправить или оставить здесь
  # это сработает после того как пользователь введёт данные
  def post(self, request):
    # мы доем все значения который пользователь ввёл в первый этап(мы получаем значение блогадаря(request.POST))
    form = FirstStepRegisterForm(request.POST)
    # если они коректны(но лучше запоминай валидный, поскольку в веб програмировании так принито) продолжет
    if form.is_valid():
      # мы данные из формы сохраняем в user но не сохраяняем в базе данных поскольку хотим в будущем дополнить
      user = form.save(commit=False)
      # пользователь ввел email и мы его домен сохраняем в этой переменной
      email_domain = form.cleaned_data.get('email').split('@')[-1]
      # если мы понимаем по домену что это абитуриент то перенаправляем в второй этап регистрации(и там мы сохраним пользователя в базе данных)
      if email_domain == 'apnt.mu':
        # пока что сохраняем в базе данных
        user.save()
        # мы id пользователя сохраняем в сесси чтобы в втором шаге понять что это тот же пользователь(для каждого пользователя отдельная сессия, и данные внем очистится(хоткей умрёт) если только выйти из сервера)
        request.session['user_id'] = user.id
        # имя шаблона, вторй шаг регистрации
        return redirect('main:second_step_registration')
      # если мы понимаем что пользователь учитель, то сохраняем его данные на базе данных
      elif email_domain == 'th.mu':
        # сохраняем данные который пользователь заполнял в формах
        user.save()
        # тут пользователь авторизируется
        login(request, user)
        # перемещяется на нужный шаблон
        return redirect('home')
    # тут должен отправлятся тот url на который сейчас пользователь, поскольку он сделал что то не так
    return render(request, 'main/registration.html', {'form': form})



# второй этап регистрации для абитуриентов, 
class SecondStepRegistrationView(View):
  # пользавателю отправляется формы чтобы он заполнил их
  def get(self, request):
    # форма который мы отпраляем
    form = SecondStepApplicantForm
    # передаем страницу шабон и форму
    return render(request, 'main/registration_step2.html', {'form': form})
  
  # данные пришли из пользователя и тут проверяестя валидный ли он
  def post(self, request):
    # передаем данные который пришли из пользователя(формы который он заполнил)
    form = SecondStepApplicantForm(request.POST, request.FILES)
    # елси он валидный то мы передаем к user и сохраняем в базе данных
    if form.is_valid():
      # мы получаем id пользователя из сесси(мы сохранили id пользователя до этого в сесси)
      user_id = request.session.get('user_id')
      # проверяется было ли получено id из сесси
      if user_id:
        try:
          # Попробуем получить существующий профиль пользователя из базы данных
          user = User.objects.get(id=user_id)
          profile = Profile.objects.get(user=user)  # Проверяем, есть ли уже профиль

          # Если профиль существует, можно обновить его данными
          profile.name = form.cleaned_data['name']
          profile.surname = form.cleaned_data['surname']
          profile.profile_picture = form.cleaned_data['profile_picture']
          profile.address_region = form.cleaned_data['address_region']
          profile.address_district = form.cleaned_data['address_district']
          profile.address_city = form.cleaned_data['address_city']
          profile.address_village = form.cleaned_data['address_village']
          profile.address_home = form.cleaned_data['address_home']
          profile.birth_year = form.cleaned_data['birth_year']
          profile.phone_number = form.cleaned_data['phone_number']
          profile.gender = form.cleaned_data['gender']
          profile.school = form.cleaned_data['school']
          profile.ort_score = form.cleaned_data['ort_score']
          profile.save()
        except ObjectDoesNotExist:
          # Если профиль не найден, создаем новый
          Profile.objects.create(
            user=user,
            name = form.cleaned_data['name'],
            surname = form.cleaned_data['surname'],
            profile_picture = form.cleaned_data['profile_picture'],
            address_region=form.cleaned_data['address_region'],
            address_district=form.cleaned_data['address_district'],
            address_city=form.cleaned_data['address_city'],
            address_village=form.cleaned_data['address_village'],
            address_home=form.cleaned_data['address_home'],
            gender=form.cleaned_data['gender'],
            birth_year=form.cleaned_data['birth_year'],
            phone_number=form.cleaned_data['phone_number'],
            ort_score=form.cleaned_data['ort_score'],
            school=form.cleaned_data['school']
          )
        
        login(request, user)  # Логиним пользователя
        # перенаправляем пользовател к url адресу
        return redirect('applicant:personal_account')
    else:
      user_id = request.session.get('user_id')
      if user_id:
        user = User.objects.get(id=user_id)
        if user:
          user.delete()  # Удаляем пользователя при неуспешной регистрации
        return redirect('first_step_registration')
    # 'это шаблон второго этапа поскольку предполагаестя что если досшло до этой строчки то условия сверху не срабоатли а значит пользователь ввел не коректные данные
    # ошибки тоже будут отпровлены с помощю формы, (в форму ошиби предал это form.is_valid())
    return render(request, 'main/registration_step2.html', {'form': form})


class LoginUserView(LoginView):
  template_name = 'main/login.html'
  form_class = CustomLoginForm

  def dispatch(self, request, *args, **kwargs):
    # проверяем авторизован ли пользователь, елси да то перенаправим нужную url адрес если нет ему придется авторизоватся
    if request.user.is_authenticated:
      email = request.user.email
      if email.endswith('@apnt.mu'):
        return redirect('applicant:personal_account')
      elif email.endswith('@th.mu'):
        return redirect('home')
      elif email.endswith('@std.mu'):
        return redirect('student:personal_account')
    
    # Если не авторизован, продолжаем обработку
    return super().dispatch(request, *args, **kwargs)

  # это сработает, и отправит форумы которые пользователь должен заполнить
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # self.get_form(CustomLoginForm)имменно это позволяет вывести ошибки который ввел пользователь
    context['form'] = self.get_form(CustomLoginForm)  # Используйте вашу кастомную форму
    return context
  
  def form_valid(self, form):
    email = form.cleaned_data.get('email')
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    
    user = authenticate(self.request, username=username, password=password)

    if user.email == email:
      if user is not None:
        login(self.request, user)

        # проверяем домен email
        if email.endswith('@apnt.mu'):
          return redirect('applicant:personal_account')
        elif email.endswith('@th.mu'):
          return redirect('home')
        elif email.endswith('@std.mu'):
          return redirect('student:personal_account')
        else:
          form.add_error('email', "Неверный домен email.")
          return self.form_invalid(form)
      else:
        form.add_error(None, "Неверные данные для входа.")
        return self.form_invalid(form)
    else:
      # Если email не совпадает, возвращаем ошибку
      form.add_error(None, "Данные не верны")
      return self.form_invalid(form)
    

  def get_success_url(self):
    return reverse_lazy('home')
  