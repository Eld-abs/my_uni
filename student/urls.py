from django.urls import path
from . import views

urlpatterns = [
  path('', views.PersonalAccountView.as_view(), name='personal_account'),
  path('profile/', views.ProfileView.as_view(), name='profile'),
  path('update_profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='update_profile'),
  path('syllabus/', views.SyllabusView.as_view(), name='syllabus'),
  path('contract/', views.ContractView.as_view(), name='contract'),
  path('schedule/', views.ScheduleView.as_view(), name='schedule'),
  path('assessments/', views.AssessmentsView.as_view(), name='assessments'),
  path('session/', views.SessionView.as_view(), name='session'),
]