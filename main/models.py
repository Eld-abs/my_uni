from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField



class Address(models.Model):
  country = models.CharField(max_length=75, verbose_name='Страна', null=False, blank=False, help_text='Введите адрес: Страна')
  region = models.CharField(max_length=75, verbose_name='Область', null=False, blank=False, help_text='Введите адрес: Область')
  city = models.CharField(max_length=75, verbose_name='Город', null=False, blank=False, help_text='Введите адрес: Город')
  district = models.CharField(max_length=75, verbose_name='Район', null=False, blank=False, help_text='Введите адрес: Район')
  street = models.CharField(max_length=75, verbose_name='Улица', null=False, blank=False, help_text='Введите адрес: Улица')
  home = models.CharField(max_length=75, verbose_name='Дом', null=False, blank=False, help_text='Введите адрес: Дом')
  apartment = models.CharField(max_length=75, verbose_name='Квартира', null=False, blank=False, help_text='Введите адрес: Квартира')

  class Meta:
    verbose_name = 'Адрес'
    verbose_name_plural = 'Факультеты'


def object_photo_path(instance, filename):
  name = instance.name.replace(' ', '_')
  type = instance.type.replace(' ', '_')
  ext = filename.split('.')[-1]
  return f'images/{type}/{name}/{instance.id}{ext}'

class ObjectInfo(models.Model):
  class TypeChoices(models.TextChoices):
    FACULTY = 'FC', 'Факультет'
    SPECIALTY = 'SP', 'Специальность'
    GROUP = 'GR', 'Группа'

  address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='object_info', null=False, blank=False)
  type = models.CharField(max_length=2, choices=TypeChoices.choices, null=False, blank=False, verbose_name='Что это за объект', help_text='Выберите один из объектов')
  name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название объекта', help_text='Введите название объекта')
  code = models.CharField(max_length=50, null=False, blank=False, verbose_name='Код объекта(аббревиатура)', help_text='Введите имя объекта')
  status = models.BooleanField(default=False, null=False, blank=False, verbose_name='Существует ли объект все ещё', help_text='Объект все ещё существует?')
  photo_1 = models.ImageField(upload_to=object_photo_path, blank=True, null=False, verbose_name='Изображение', help_text='Загрузите фото в формате JPG, или PNG', default='defaults/no-images-object.png')
  photo_2 = models.ImageField(upload_to=object_photo_path, blank=True, null=False, verbose_name='Изображение', help_text='Загрузите фото в формате JPG, или PNG', default='defaults/no-images-object.png')
  description = models.CharField(max_length=250, null=False, blank=False, verbose_name='Описание', help_text='Краткое описание объекта')
  about_as = models.TextField(max_length=800, null=False, blank=False, verbose_name='Описание длинные', help_text='Подробная описание объекта')
  date_formation = models.DateField(null=False, blank=False, verbose_name='Дата формирование', help_text='Выберите дату когда это было создано')


class Faculty(models.Model):
  object_info = models.OneToOneField(ObjectInfo, on_delete=models.CASCADE, related_name='faculty', null=False)
  educational_process = models.BooleanField(default=False, null=False, blank=True, verbose_name='Учебный процесс', help_text='Укажите идет ли учебный процесс')

  class Meta:
    verbose_name = 'Факультет'
    verbose_name_plural = 'Факультеты'

  def __str__(self):
    return self.object_info.name


class Specialty(models.Model):
  class EducationTypeChoices(models.Choices):
    FULL_TIME = 'FT', 'Очное'
    CORRESPONDENCE_EDUCATION = 'CE', 'Заочное'
    ALL = 'AL', 'Очное и заочное'
  
  object_info = models.OneToOneField(ObjectInfo, on_delete=models.CASCADE, related_name='specialty', null=False)
  faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='specialty', null=False)
  budget_place_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=False)
  education_type = models.CharField(max_length=2, choices=EducationTypeChoices.choices, null=False, blank=False, verbose_name='Тип обучение(очный, заочный или оба)', help_text='Выберите тип обучение')
  min_ort_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(245)])
  duration_years = models.IntegerField(
                  validators=[MinValueValidator(1), MaxValueValidator(10)],verbose_name="Длительность обучения (лет)")
  contract = models.IntegerField(verbose_name="Размер контракта", validators=[MinValueValidator(0)], default=0)

  class Meta:
    verbose_name = 'Специальность'
    verbose_name_plural = 'Специальности'
  
  def __str__(self):
    return self.object_info.name


class Lesson(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=250, null=True, blank=False)

  class Meta:
    verbose_name = 'Урок'
    verbose_name_plural = 'Уроки'

  def __str__(self):
    return self.name

  
class LessonAndSpecialty(models.Model):
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_and_specialty', null=False)
  specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='lesson_and_specialty', null=False)
  obligatory = models.BooleanField(default=False, null=False, blank=False, verbose_name='Обязательный ли этот урок для этой специальности', help_text='Выберите обязательный ли урок для группы')
  semesters = ArrayField(models.PositiveIntegerField(), blank=True, default=list, verbose_name='В каких семестрах будет преподаётся этот урок', help_text='Введите список семестров, например: [1, 2, 3]')
  price = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)], verbose_name='Цена урока, в сомах', help_text='Введите сколько стоит этот урок в сомах')
  loans = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)], verbose_name='Кредиты', help_text='Введите сколько кредитов для этого урока')

  class Meta:
    verbose_name = 'Урок'
    verbose_name_plural = 'Уроки'

  def __str__(self):
    return f'{self.lesson.name} для {self.specialty.object_info.name}'


class Group(models.Model):
  specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='group', null=False)
  object_info = models.OneToOneField(ObjectInfo, on_delete=models.CASCADE, related_name='group', null=False)
  curator = models.CharField(max_length=255, default=None, null=True ,blank=True)
  
  class Meta:
    verbose_name = 'Группа'
    verbose_name_plural = 'Группы'
  
  def __str__(self):
    return f"{self.object_info.code} {self.object_info.name}"


class Department(models.Model):
  specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='department', null=False)
  object_info = models.OneToOneField(ObjectInfo, on_delete=models.CASCADE, related_name='department', null=False)
  
  class Meta:
    verbose_name = 'Кафедра'
    verbose_name_plural = 'Кафедры'

  def __str__(self):
    return f"{self.object_info.code} {self.object_info.name}"


class Profile(models.Model):
  class RoleChoices(models.TextChoices):
    STUDENT = 'ST', 'Студент'
    APPLICANT = 'AP', 'Абитуриент'
    TEACHER = 'TH', 'Преподаватель'

  # устанавливаем связь между user и profile, но пользователь не может быть связан другой Profile благодаря OneToOneField(но можно создать другой Например Address и связать с пользователям)
  # (User, on_delete=models.CASCADE) связь будет с User, если удалят User то его профиль тоже удалится
  user = models.OneToOneField(User, on_delete=models.CASCADE) # связь с моделью User
  address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='object_info', null=False, blank=False)
  name = models.CharField(max_length=250, null=False, blank=False)
  surname = models.CharField(max_length=250, null=False, blank=False)
  profile_picture = models.ImageField(upload_to=f'imgs/profile_pictures/{id}_{name}', null=True, blank=False)
  status = models.BooleanField(default=False, null=False, blank=False, verbose_name='Все ещё в этом универе', help_text='Пользователь все ещё в универе?')
  role = models.CharField(max_length=2, choices=RoleChoices.choices, null=False, blank=False, verbose_name='Какой это пользователь', help_text='Кто этот пользователь?')
  gender = models.CharField(max_length=250, null=False, blank=False)
  birth_year = models.DateField(null=False, blank=False)
  phone_number = models.CharField(max_length=250)

  def __str__(self):
    return self.name
  
  # создает абсолютный url(так говорится в чат гпт), что я понял: reverse ищет url с именем update_profile, и когда требуется id, точнее когда этот url будет работать, и он будет искать значение id мы в него передаем id благодаря этому: ={'pk': self.id}
  def get_absolute_url(self):
    return reverse('update_profile', kwargs={'pk': self.pk})

  class Meta:
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'


class LessonAndGroup(models.Model):
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_and_group', null=False)
  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson_and_group', null=False)
  teacher = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson_and_group', null=False)


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
