
from main.models import Profile, StudentData
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
import logging



# получает пользователя, отправляем пользователя и его профиль
class ProfileService:
  @staticmethod
  def get_profile(user: User):
    try:
      profile = Profile.objects.get(user=user)
      return profile
    except Profile.DoesNotExist:
      return None


# для работы с StudentData(для создания, обновления, нахождения)
class StudentDataService:
  # получаем нужные значения для model(для сохранения в базе данных)
  @staticmethod
  def create_student_data(user, group, start_date, end_date):
    return StudentData.objects.create(
      user=user,
      group=group,
      start_date=start_date,
      end_date=end_date
    )
  
  # Принимает id объекта и словарь, и обновит поля в базе данных StudentData
  @staticmethod
  def update_student_data(user, update_fields):
    student_data = StudentData.objects.get(user=user)
    for key, value in update_fields.items():
      setattr(student_data, key, value)
    student_data.save()
    return student_data
  
  # получаем user возвращаем (кортеж) временную или обычную группу, и подсказку временная или обычная
  @staticmethod
  def get_group_or_temporary_group(user):
    try:
      student_data = get_object_or_404(StudentData, user=user)
    except StudentData.DoesNotExist:
      logging.error(f"Данные для студента с id {user.id} не найдены.")
      raise Http404("Student data not found")

    if student_data.temporary_group:
      return student_data.temporary_group, 'temporary'
    elif student_data.group:
      return student_data.group, 'regular'
  
  # получаем user, возвращает группу(временную или обычную) и код или "группы пока не распределены"
  @staticmethod
  def get_major_and_group_code(user):
    group, group_type = StudentDataService.get_group_or_temporary_group(user)
    major = group.name
    if group_type == 'temporary':
      group_code = 'Группы пока не распределены'
    elif group_type == 'regular':
      group_code = group.code
    return major, group_code
  
  # получает id и находит student_data(объект) и возвращает
  @staticmethod
  def get_student_data(user):
    try:
      return get_object_or_404(StudentData, user=user)
    except StudentData.DoesNotExist:
      logging.error(f"Данные для студента с id {user.id} не найдены.")
      raise Http404("Student data not found")
  

class FacultyService:
  # получаем id пользователя, возвращаем факультет этого 
  @staticmethod
  def get_faculty(user):
    try:
      student_data = get_object_or_404(StudentData, user=user)
    except StudentData.DoesNotExist:
      logging.error(f"Данные для студента с id {user.id} не найдены.")
      raise Http404("Student data not found")
    if student_data.temporary_group:
      faculty = student_data.temporary_group.faculty
    elif student_data.group:
      faculty = student_data.group.faculty
    else:
      logging.error(f"Факультет для пользователя {user} не найден.")
      raise Http404("Факультет не найден")
    return faculty
  

# класс работает моделью Lessons(для отправки уроков)
class LessonsService:
  # получает user отправляет уроки который преподают к этому user
  @staticmethod
  def get_lessons(user):
    group_or_temporary_group, code_group= StudentDataService.get_major_and_group_code(user)
    lessons = group_or_temporary_group.lessons

    return lessons