from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from main.models import Profile
from student.mixins import ProfileRequiredMixins
from student.services import ProfileService



class PersonalAccountView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/personal_account.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  

class ProfileView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/profile.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  

class ProfileUpdateView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/profile_update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  

class SyllabusView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/syllabus.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context


class SyllabusForGroupView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/syllabus_for_group.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  
  
class SyllabusForGroupAddView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/syllabus_for_group_add.html'

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
  template_name = 'teacher/schedule.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  

class FindStudentsView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'profile'
  template_name = 'teacher/find_students.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context
  

class GroupScheduleView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'pr0file'
  template_name = 'teacher/group_schedule.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context


class GroupScheduleSpecificView(ProfileRequiredMixins, ListView):
  model = Profile
  context_object_name = 'pr0file'
  template_name = 'teacher/group_schedule_specific.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    profile = ProfileService.get_profile(user)

    context['user'] = user
    context['profile'] = profile
    return context