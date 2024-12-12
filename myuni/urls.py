
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('student/', include(('student.urls', 'student'), namespace='student')),
    path('applicant/', include(('applicant.urls', 'applicant'), namespace='applicant')),
    path('teacher/', include(('teacher.urls', 'teacher'), namespace='teacher'))
]
