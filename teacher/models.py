from django.db import models
from main.models import Profile, Department, Lesson
from django.core.validators import MinValueValidator, MaxValueValidator

class Teacher(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='teacher', null=False, blank=False)
  department = models.OneToOneField(Department, on_delete=models.DO_NOTHING, related_name='teacher', null=False, blank=False)
  lesson = models.ManyToManyField(Lesson, related_name='teacher', null=False, blank=False)
  salary = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(500000.0)], null=True, blank=True, default=0.0, verbose_name='Зарплата', help_text='Введите зарплату сотрудника')