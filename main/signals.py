# в этом файле обрабатываются сигналы(можно проверять если что то изменяемся)
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Faculty, GroupStudents
from applicant.services import GroupServices, BudgetApplicantsGoGroupsServices


# Сигнал для создания профиля пользователя после регистрации
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)


# Сигнал для сохранения профиля пользователя при обновлении
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()


# Сигнал для того чтобы создавался нужное количество групп автоматически смотря сколько студентов,
@receiver(post_save, sender=Faculty)
def close_enrollment_and_create_group(sender, instance, **kwargs):
  if not instance.is_enrollment_open:
    # получаем список групп котору которых одинаковые факультеты(тот факультет который закончил набор)
    temporary_groups = GroupStudents.objects.filter(faculty=instance)

    # добавляем бюджетников(абитуриентов) в временные группы(после этого они вместо с остальными вступят в обычные группы)
    BudgetApplicantsGoGroupsServices.call_method_by_queue(temporary_groups)
    
    # делает работу: создает группы, даёт им нужные данные, перенаправляет студентов(из временной группы в обычный)
    GroupServices.how_many_groups_we_need(temporary_groups)
    


    