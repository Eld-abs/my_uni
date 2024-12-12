from django.urls import path
from . import views

urlpatterns = [
  path('', views.PersonalAccount.as_view(), name='personal_account'),
  path('update_profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='update_profile'),
  path('faculties/', views.FacultyListView.as_view(), name='faculty_list'),
  path('faculties/<int:faculty_id>/groups/', views.GroupListView.as_view(), name='group_list'),
  path('groups/<int:group_id>/lessons/', views.LessonListView.as_view(), name='lesson_list'),
  path('budget_places/<int:temporary_group_id>', views.BudgetPlacesView.as_view(), name='budget_places'),
]

