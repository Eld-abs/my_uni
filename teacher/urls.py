from django.urls import path
from . import views

urlpatterns = [
  path('', views.PersonalAccountView.as_view(), name='personal_account'),
  path('profile/', views.ProfileView.as_view(), name='profile'),
  path('profile_update/', views.ProfileUpdateView.as_view(), name='profile_update'),
  path('syllabus/', views.SyllabusView.as_view(), name='syllabus'),
  path('syllabus_for_group/', views.SyllabusForGroupView.as_view(), name='syllabus_for_group'),
  path('syllabus_for_group/add/', views.SyllabusForGroupAddView.as_view(), name='syllabus_for_group_add'),
  path('schedule/', views.ScheduleView.as_view(), name='schedule'),
  path('find_students/', views.FindStudentsView.as_view(), name='find_students'),
  path('group_schedule/', views.GroupScheduleView.as_view(), name='group_schedule'),
]