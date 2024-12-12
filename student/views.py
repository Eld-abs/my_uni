from django.middleware.csrf import get_token
from main.models import Profile
from django.views.generic import ListView, UpdateView
from main.forms import ProfileUpdateForm
from django.urls import reverse_lazy
from student.services import ProfileService, FacultyService, StudentDataService
from student.mixins import ProfileRequiredMixins



class PersonalAccountView(ProfileRequiredMixins, ListView):
  model = Profile
  template_name = 'student/personal_account.html'
  context_object_name = 'profile'

  # отправляет данные(пользователя и его профиль) к шаблону
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    profile = ProfileService.get_profile(user)
    faculty = FacultyService.get_faculty(user)
    student_data = StudentDataService.get_student_data(user)
    group_name, group_code = StudentDataService.get_major_and_group_code(user)
    context['user'] = user
    context['profile'] = profile
    context['faculty'] = faculty
    context['group_name'] = group_name
    context['group_code'] = group_code
    context['student_data'] = student_data
    return context



class ProfileView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'student/profile.html'
  
  # отправляет данные(пользователя и его профиль) к шаблону
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    profile = ProfileService.get_profile(user)
    faculty = FacultyService.get_faculty(user)
    student_data = StudentDataService.get_student_data(user)
    group_name, group_code = StudentDataService.get_major_and_group_code(user)
    context['user'] = user
    context['profile'] = profile
    context['faculty'] = faculty
    context['group_name'] = group_name
    context['group_code'] = group_code
    context['student_data'] = student_data
    return context


class ProfileUpdateView(ProfileRequiredMixins, UpdateView):
  model = Profile
  template_name = 'student/profile_update.html'
  form_class = ProfileUpdateForm
  # revarse_lazy делает строкой url адрес который находит (по имени personal_account)
  success_url = reverse_lazy('student:personal_account')

  # возвращает пользователя если он понадобится
  def get_object(self):
    user = self.request.user
    return Profile.objects.get(user=user)
  
    # отправляет данные(пользователя и его профиль) к шаблону
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    profile = ProfileService.get_profile(user)
    faculty = FacultyService.get_faculty(user)
    student_data = StudentDataService.get_student_data(user)
    group_name, group_code = StudentDataService.get_major_and_group_code(user)
    context['user'] = user
    context['profile'] = profile
    context['faculty'] = faculty
    context['group_name'] = group_name
    context['group_code'] = group_code
    context['student_data'] = student_data
    return context
  
  def form_valid(self, form):
    response = super().form_valid(form)
    return response
  
  def form_invalid(self, form):
    print("Форма невалидна")  # Отладка
    print(form.errors)  # Вывод ошибок формы
    return super().form_invalid(form)
  

class SyllabusView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'student/syllabus.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    profile = ProfileService.get_profile(user)

    # lessons = LessonsService.get_lessons(user)

    context['user'] = user
    context['profile'] = profile
    # работа приостановлена 
    # context['lessons'] = lessons
    return context


class ContractView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'student/contract.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context


class ScheduleView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'student/schedule.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  

class AssessmentsView(ProfileRequiredMixins, ListView):
  model = Profile 
  context_object_name = 'profile'
  template_name = 'student/assessments.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  
class SessionView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'student/session.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context