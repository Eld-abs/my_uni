from django.contrib import admin
from .models import Faculty, Group, Lesson, Profile, StudentData, GroupStudents
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.db import models
from django.forms import Textarea



# мы удаляем старый вывод инфорамации на понели админа
# Удалите стандартную регистрацию модели User, если она уже зарегистрирована
if admin.site.is_registered(User):
    admin.site.unregister(User)


class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'address_city', 'birth_year', 'phone_number')  # Поля, которые будут отображаться в админке
  search_fields = ('user__username', 'address_region')  # Поиск по имени пользователя и адресу

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Faculty)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(StudentData)
admin.site.register(GroupStudents)


# мы указываем что дополним нужную ___ с дополнением, это самое дополнение мы указываем в этом классе
class ProfileInline(admin.StackedInline):
    # мы будем дополнять с профилем
    model = Profile
    # в моделе есть поле 'user' это мы и будем дополнять этот объект с model который мы указали сверху(model = Profile)
    fk_name = 'user'
    # мы говорим что в понели администратора мы запрещяем уалять profile
    can_delete = False
    # в понеле администратора это будет так показона(вроде, это не очень важно по этому я не иследовал)
    verbose_name_plural = 'Profile'


# создаем кастомный класс, как будет выведено данные в понеле администратора
class CustomUserAdmin(DefaultUserAdmin):
    # говорим какое дополнение будет добавлено(тот класс который мы создали)
    inlines = (ProfileInline, )

    # Переопределяем метод get_queryset, чтобы оптимизировать запросы. Мы используем select_related('profile'), чтобы при получении объектов User сразу подтягивать связанные записи из модели Profile. Это уменьшает количество запросов к базе данных, когда мы обращаемся к полям профиля через пользователя.
    def get_queryset(self, request):
        # простыми словами это оптимизирует но как я хз
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('profile')
        return queryset
    
    # создаем метод который будет выводить на панель админку то что мы возьмом из этого метода
    def profile_ort_score(self, instance):
        # получаем балл по ОРТ и отправляем чтобы было выведено в понели администратора
        return instance.profile.ort_score
    
    # будет отображатся в панели одминистратора как заголовок
    profile_ort_score.short_description = 'ort_score'

    # список данных которые будут выводится в понели администратора(тут есть тот метод который мы создали)
    list_display = ('username', 'email', 'first_name', 'last_name', 'profile_ort_score')
    # мы делаем один запрос на сервер и сразу возьмом все профили из базы данных, и когда будет нужно не нужно будет обращятся к серверу, (напрмер есть 100 пользователей, мы возьмом их профили и сохраним делая только 1 запрос на сервер)(если бы не это было бы 100 запросов для каждого пользователя)
    list_select_related = ('profile', )


admin.site.register(User, CustomUserAdmin)

class GroupStudentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'min_ort_score', 'duration_years', 'all_students', 'contract')
    search_fields = ('name', 'faculty__name')
    list_filter = ('faculty', 'duration_years')
    ordering = ('name',)
    
    formfield_overrides = {
        models.JSONField: {'widget': Textarea(attrs={'cols': 80, 'rows': 20})},  # Используем Textarea
    }

    fieldsets = (
        (None, {
            'fields': ('name', 'faculty', 'min_ort_score', 'photo', 'description', 'duration_years', 'all_students', 'contract', 'details')
        }),
    )

# class GroupStudentsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'faculty', 'min_ort_score', 'duration_years', 'all_students', 'contract')
#     search_fields = ('name', 'faculty__name')
#     list_filter = ('faculty', 'duration_years')
#     ordering = ('name',)
    
#     formfield_overrides = {
#         models.JSONField: {'widget': admin.widgets.AdminJSONWidget()},
#     }

#     fieldsets = (
#         (None, {
#             'fields': ('name', 'faculty', 'min_ort_score', 'photo', 'description', 'duration_years', 'all_students', 'contract', 'details')
#         }),
#     )

# # Регистрируем модель и её админский класс
# admin.site.register(GroupStudents, GroupStudentsAdmin)

