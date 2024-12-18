from django.db import models
from main.models import Profile, Specialty
from django.core.validators import MinValueValidator, MaxValueValidator

class Applicant(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='teacher', null=False)
  specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='lesson_and_specialty', null=False)
  form_of_training = models.CharField(max_length=250, null=True, blank=False)
  school = models.CharField(max_length=200, null=True, blank=False)
  ort_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(245)], max_length=200, null=True, blank=False)

  class Meta:
    verbose_name = 'Абитуриент'
    verbose_name_plural = 'Абитуриенты'

  def __str__(self):
    return self.profile.name