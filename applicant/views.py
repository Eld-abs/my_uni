from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from main.models import Faculty, GroupStudents, Lesson, Profile, StudentData
from main.forms import ProfileUpdateForm, FormOfTraining
from applicant.services import BudgetPlacesServices, ProfileServices, ApplicantAdnStudentServices



# Личный кабинет
class PersonalAccount(DetailView):
  model = Profile
  template_name = 'applicant/personal_account.html'
  context_object_name = 'profile'

  def get_object(self):
    user = self.request.user
    return Profile.objects.get(user=user)


# Обновить данные 
class ProfileUpdateView(UpdateView):
  model = Profile
  template_name = 'applicant/update_profile.html'
  form_class = ProfileUpdateForm
  # revarse_lazy находит и делает строкой url адрес по имени personal_account
  success_url = reverse_lazy('applicant:personal_account')
  
  # возвращает пользователя если он понадобится
  def get_object(self):
    user = self.request.user
    return Profile.objects.get(user=user)
  
  def form_valid(self, form):
    response = super().form_valid(form)
    return response
  
  def form_invalid(self, form):
    print("Форма невалидна")  # Отладка
    print(form.errors)  # Вывод ошибок формы
    return super().form_invalid(form)


# Факультеты
class FacultyListView(ListView):
  model = Faculty
  template_name = 'applicant/faculties.html'
  context_object_name = 'faculties'


# список групп выбранного факультета
class GroupListView(ListView):
  model = GroupStudents
  template_name = 'applicant/groups.html'
  context_object_name = 'groups'

  # находим нужные группы и отправляем к странице
  def get_queryset(self):
    faculty = get_object_or_404(Faculty, pk=self.kwargs['faculty_id'])
    groups = GroupStudents.objects.filter(faculty=faculty)
    return groups

  # отправляем в контексте нужный нам факультет чтобы отобразить данные
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    faculty = get_object_or_404(Faculty, pk=self.kwargs['faculty_id'])
    context['faculty'] = faculty
    return context


# список уроков выбранной группы
class LessonListView(ListView):
  model = Lesson
  template_name = 'applicant/lessons.html'
  context_object_name = 'lessons'

  # находим нужную группу, и уроки этой группы отправляем к странице
  def get_queryset(self):
    group = get_object_or_404(GroupStudents, pk=self.kwargs['group_id'])
    return Lesson.objects.filter(group_students=group)

  # находим нужную группу и отправляем
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    group = get_object_or_404(GroupStudents, pk=self.kwargs['group_id'])
    how_percent = group.budget_place_percent
    how_many_applicants_no_budget = group.students_data.count()
    budget_places = BudgetPlacesServices.get_how_math_budgets_place(how_percent, how_many_applicants_no_budget)

    context['group'] = group
    context['budget_places'] = budget_places
    return context

  # проверяем достаточно ли баллов для нужной группы у студента
  def post(self, request, *args, **kwargs):
    temporary_group = get_object_or_404(GroupStudents, pk=kwargs['group_id'])
    user = request.user
    profile = Profile.objects.get(user=user)
    form = FormOfTraining(request.POST)

    if ApplicantAdnStudentServices.is_eligible_for_group(profile, temporary_group):
      if form.is_valid():
        form_of_training = form.cleaned_data['form_of_training']

        ApplicantAdnStudentServices.update_user_email(user)
        ApplicantAdnStudentServices.create_student_data(user, temporary_group, form_of_training)

        messages.success(request, "Вы успешно вступили группу")
        return redirect('student:personal_account')
      else:
        messages.error(request, "Ошибка в форме, выберите один из вариантов")
        return redirect('applicant:lesson_list', group_id=temporary_group.id)
    else:
      messages.error(request, f"У вас не достаточно ОРТ баллов для этой группы, ваш балл: {profile.ort_score}, требуемый минимум: {temporary_group.min_ort_score}")
      return self.get(request, *args, **kwargs)  

    
class BudgetPlacesView(ListView):
  model = GroupStudents
  template_name = 'applicant/budget_places.html'
  context_object_name = 'budget_places'

  # отправляет данные: временную группу и список мест
  def get_context_data(self, **kwargs):
    user = self.request.user
    context = super().get_context_data(**kwargs)
    temporary_group_id = self.kwargs.get('temporary_group_id')
    temporary_group = GroupStudents.objects.filter(pk=temporary_group_id).first()

    how_percent = temporary_group.budget_place_percent
    how_many_applicants_no_budget = temporary_group.students_data.count()
    budget_places = BudgetPlacesServices.get_how_math_budgets_place(how_percent, how_many_applicants_no_budget)
    is_budget_application = BudgetPlacesServices.is_budget_application_active(user, temporary_group)
    applicants = ProfileServices.applicants_who_wont_to_budget(temporary_group_id)

    context['group'] = temporary_group
    context['budget_places'] = 2
    context['is_budget_application'] = is_budget_application
    context['applicants'] = applicants
    return context

  # кода абитуриент нажал что хочет побороться за место в бюджете: связывает user and budgetapplicants,
  def post(self, request, *args, **kwargs):
    user = self.request.user
    temporary_group_id = self.kwargs.get('temporary_group_id')
    temporary_group = GroupStudents.objects.filter(pk=temporary_group_id).first()

    BudgetPlacesServices.toggle_budget_application(user, temporary_group)
    return redirect('applicant:budget_places', temporary_group_id=temporary_group_id)