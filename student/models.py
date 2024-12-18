from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from main.models import Group, Lesson, Attendance
from applicant.models import Applicant

class Student(models.Model):
  applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name='student', null=False)
  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='student', null=False)
  date_start = models.DateField(null=False, blank=True)
  date_end = models.DateField(null=False, blank=True)

  class Meta:
    verbose_name = 'Студент'
    verbose_name_plural = 'Студенты'

  def __str__(self):
    return self.applicant.profile.name
  

class Module(models.Model):
  student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='module', null=False)
  lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='module', null=False)
  module = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True)
  max_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)], null=True)
  score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)], null=True)

  class Meta:
    verbose_name = 'Модуль'
    verbose_name_plural = 'Модули'

  def __str__(self):
    return f'Модуль студента {self.student.applicant.profile.name}'
  

class StudentAttendance(models.Model):
  attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='student_attendance', null=False)
  student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance', null=False)
  is_present = models.BooleanField(default=False, null=False, blank=False)
  score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

  class Meta:
    verbose_name = 'Модуль'
    verbose_name_plural = 'Модули'

  def __str__(self):
    return f'Посещаемость студента {self.student.applicant.profile.name}'