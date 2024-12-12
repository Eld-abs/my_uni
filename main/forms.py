from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import StudentData, Profile



# первая форма для регистрации
class FirstStepRegisterForm(UserCreationForm):
  username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Введите логин'}))
  password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'custom-form', 'placeholder': 'Введите пароль'}))
  password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'custom-form', 'placeholder': 'Повторите пароль'}))
  email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'custom-form', 'placeholder': 'Введите email'}))

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

  def save(self, commit=True):
    user = super(FirstStepRegisterForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.save()
    return user
    
  def clean_email(self):
    email = self.cleaned_data.get('email')
    allowed_domains = ['apnt.mu', 'th.mu']  # Разрешённые домены

    # Проверяем домен email
    domain = email.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError("Регистрация доступна только для доменов @apnt.mu и @th.mu")
    
    return email
  

# второй этап регистрации
class SecondStepApplicantForm(forms.Form):
  name = forms.CharField(label='Имя', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Имя'}))
  surname = forms.CharField(label='Фамилия', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Фамилия'}))
  # СПРОСИ ЧАТА МОЖНО ЛИ СЮДА ДОБАВИТЬ КЛАСС ДЛЯ СТИЛЕЙ
  profile_picture = forms.ImageField(label='Фото профиля', required=False)
  address_region = forms.CharField(label='Область', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Область'}))
  address_district = forms.CharField(label='Район', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Район'}))
  address_city = forms.CharField(label='Город', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Город'}))
  address_village = forms.CharField(label='Село', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Село'}))
  address_home = forms.CharField(label='Дом', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Дом'}))
  gender = forms.ChoiceField(label='Гендер', choices=[('man', 'мужчина'), ('woman', 'женщина')], widget=forms.RadioSelect(attrs={'class': 'custom-form gender-choice', 'placeholder': 'выберите пол'}))
  school = forms.CharField(label='Школа', required=True, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Имя №номер'}))
  # если бы мы выключим required=False то это поле будет не обизательным
  birth_year = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'custom-form', 'placeholder': 'ДД.ММ.ГГГГ'}, format='%d.%m.%Y'))
  phone_number = forms.CharField(label='Номер телефона', required=False, widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': '+996700102030' }))
  ort_score = forms.IntegerField(label='Основной балл по ОРТ', required=True, widget=forms.NumberInput(attrs={'class':'custom-form','placeholder': 'Введите балл по ОРТ(основной)'}))

# Обновляем данные пользователя(форма для него)
class ProfileUpdateForm(forms.ModelForm):
  gender = forms.ChoiceField(
    label='пол',
    choices=[('мужчина', 'мужчина'), ('женщина', 'женщина')],
    widget=forms.RadioSelect(attrs={'class': 'custom-form gender-choice'})
    )
  ort_score = forms.IntegerField(
    label='ОРТ балл',
    widget=forms.NumberInput(attrs={
      'class': 'custom-form',
      'readonly': 'readonly',  # делаем поле только для чтения
      'placeholder': 'ОРТ балл'
    })
    )
  class Meta:
    model = Profile
    fields = [
      'name', 'surname', 'profile_picture', 'address_region', 'address_district', 'address_city', 'address_village', 'address_home','gender', 'school', 'birth_year', 'phone_number', 'ort_score'
    ]
    widgets = {
      'name': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Имя'}),
      'surname': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Фамилия'}),
      'profile_picture': forms.ClearableFileInput(attrs={'class': 'custom-form'}),
      'address_region': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Область'}),
      'address_district': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Район'}),
      'address_city': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Город'}),
      'address_village': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Село'}),
      'address_home': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Дом'}),
      'gender': forms.RadioSelect(attrs={'class': 'custom-form gender-choice'}),
      'school': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Школа'}),
      'birth_year': forms.DateInput(attrs={'class': 'custom-form', 'placeholder': 'ДД.ММ.ГГГГ'}, format='%d.%m.%Y'),
      'phone_number': forms.TextInput(attrs={'class': 'custom-form', 'placeholder': '+996700102030'}),
      'ort_score': forms.NumberInput(attrs={'class': 'custom-form', 'placeholder': 'Введите балл по ОРТ(основной)'}),
    }


# форма для страницы регистрации
class CustomLoginForm(AuthenticationForm):
  username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'custom-form', 'placeholder': 'Введите логин'}))
  password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'custom-form', 'placeholder': 'Введите пароль'}))
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'custom-form', 'placeholder': 'Введите email'}))

  # проверяет email(пустой или нет)
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if not email:
      raise ValidationError('Введите email.')
    return email

  # проверяет есть ли такой пользователь и совподает ли пороль и логин с email
  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')

    if email and username and password:
      from django.contrib.auth import authenticate
      user = authenticate(username=username, password=password)
      if user is None:
        raise ValidationError("Логин или пароль неверны!")
      if user is None or user.email != email:
        raise ValidationError("email не совподает с данными который вы ввели!")
    
    return cleaned_data


class FormOfTraining(forms.ModelForm):
    form_of_training = forms.ChoiceField(
    label='форма обучение',
    choices=[('Очный', 'Очный'), ('Заочный', 'Заочный')],
    widget=forms.RadioSelect(attrs={'class': 'custom-form gender-choice'})
    )

    class Meta:
      model = StudentData
      fields = ['form_of_training']
      
      widgets = {
        'form_of_training': forms.RadioSelect(attrs={'class': 'custom-form gender-choice'})
      }



# форма для вывода формы чтобы заполнить информацеей про студента(только то что касается к универу, данные типо адрес дома тут нет)
class StudentDataForm(forms.ModelForm):
  # тут мы можем указать как будет выглидеть формы в шаблоне, тут мы можем добавить класс и стили
  start_date = forms.DateField(
    widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'дд.мм.гггг'}))
  end_date = forms.DateField(
    widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'дд.мм.гггг'}))

  class Meta:
    # используем как модель StudentData который мы создали
    model = StudentData
    # в странице будут эти формы чтобы он их заполнил
    fields = ['start_date', 'end_date',]
  
  # мы проверяем, тот кто введёт данные для пользователя тут будет добовлять ошибку
  def clean(self):
    cleaned_data = super().clean()
    start_date = cleaned_data.get('start_date')
    end_date = cleaned_data.get('end_date')

    if start_date and end_date:
      if end_date < start_date:
        self.add_error('end_date', 'Дата окончания не может быть раньше даты начала.')

    return cleaned_data