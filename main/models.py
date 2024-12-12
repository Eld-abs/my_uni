from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse



class Faculty(models.Model):
  name = models.CharField(max_length=100)
  photo = models.ImageField(upload_to='faculty/photo', null=True, blank=False)
  description = models.CharField(max_length=250, null=True, blank=False)
  is_enrollment_open = models.BooleanField(default=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Факультет'
    verbose_name_plural = 'Факультеты'


class GroupStudents(models.Model):
  name = models.CharField(max_length=100)
  faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='groups')
  min_ort_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
  photo = models.ImageField(upload_to='group/photo', null=True, blank=False)
  photo_2 = models.ImageField(upload_to='group/photo', null=True, blank=False)
  budget_place_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=False)
  duration_years = models.IntegerField(
                  validators=[MinValueValidator(1), MaxValueValidator(10)],verbose_name="Длительность обучения (лет)")
  contract = models.IntegerField(verbose_name="Размер контракта", validators=[MinValueValidator(0)], default=0)
  details = models.JSONField(null=True, blank=True)
  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Группа(временная)'
    verbose_name_plural = 'Группы(временные)'


class Lesson(models.Model):
  name = models.CharField(max_length=100)
  group_students = models.ManyToManyField(GroupStudents, related_name='lessons',  blank=True)
  description = models.CharField(max_length=250, null=True, blank=False)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Урок'
    verbose_name_plural = 'Уроки'
  

class BudgetApplicants(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_applicants')
  temporary_group = models.ForeignKey(GroupStudents, on_delete=models.CASCADE, related_name='budget_applicants')
  applicant_wont_to_budget = models.BooleanField(default=False)

  class Meta:
    verbose_name = 'Хочет ли абитуриент вступить в эту группу' 
    verbose_name_plural = 'Хотят ли абитуриенты вступить в эту группу'


class Group(models.Model):
  name = models.CharField(max_length=100)  # Имя группы
  faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='actual_groups')  # Связь с факультетом
  min_ort_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])  # Минимальный ОРТ
  duration_years = models.IntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Длительность обучения (лет)", default=4)  # Длительность обучения
  code = models.CharField(max_length=100, default='default_code')
  curator = models.CharField(max_length=255, default=None, blank=True)
  lessons = models.ManyToManyField(Lesson, related_name='groups', blank=True)
  contract = models.IntegerField(verbose_name="Размер контракта", validators=[MinValueValidator(0)], default=0)
  
  def __str__(self):
    return f"{self.code} {self.name}"
  
  class Meta:
    verbose_name = 'Группа'
    verbose_name_plural = 'Группы'


class Profile(models.Model):
  # устанавливаем связь между user и profile, но пользователь не может быть связан другой Profile благодаря OneToOneField(но можно создать другой Например Address и связать с пользователям)
  # (User, on_delete=models.CASCADE) связь будет с User, если удалят User то его профиль тоже удалится
  user = models.OneToOneField(User, on_delete=models.CASCADE) # связь с моделью User
  name = models.CharField(max_length=250, null=True, blank=False)
  surname = models.CharField(max_length=250, null=True, blank=False)
  profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=False)
  address_region = models.CharField(max_length=250, null=True, blank=False)
  address_district = models.CharField(max_length=250, null=True, blank=False)
  address_city = models.CharField(max_length=250, null=True, blank=False)
  address_village = models.CharField(max_length=250, null=True, blank=False)
  address_home = models.CharField(max_length=250, null=True, blank=False)
  gender = models.CharField(max_length=250, null=True, blank=False)
  birth_year = models.DateField(null=True)
  phone_number = models.CharField(max_length=250)
  school = models.CharField(max_length=250)
  ort_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], null=True)
  is_completed = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username
  
  # создает абсолютный url(так говорится в чат гпт), что я понял: reverse ищет url с именем update_profile, и когда требуется id, точнее когда этот url будет работать, и он будет искать значение id мы в него передаем id благодаря этому: ={'id': self.id}
  def get_absolute_url(self):
    return reverse('update_profile', kwargs={'pk': self.pk})

  class Meta:
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'


class StudentData(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_data')
  group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='students_data', null=True)
  temporary_group = models.ForeignKey(GroupStudents, on_delete=models.SET_NULL, related_name='students_data', null=True)
  start_date = models.DateField()
  end_date = models.DateField()
  form_of_training = models.CharField(max_length=250, null=True, blank=False)

  def __str__(self):
    return self.user.username
   
  class Meta:
    verbose_name = 'Информация студента(связанные с университетом)'
    verbose_name_plural = 'Информации студентов(связанные с университетом)'
