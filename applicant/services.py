from main.models import Profile, GroupStudents, BudgetApplicants, StudentData, Group
import datetime



# Класс работает profile
class ProfileServices:
  # с помощью @staticmethod мы можем работать с методам даже если у класса ProfileServices нет объекта
  @staticmethod
  def update_profile(profile, form_data):
    # логика обновления профиля
    for key, value in form_data:
      # принимает 3 значение, 1(изменяет или добавляет к этому) 2(находит это поле, если не находит создает такое и) 3(это значение которое даётся)
      setattr(profile, key, value)
    profile.save()

  # получает id временной группы, возвращает абитуриентов которые хотят в бюджет
  @staticmethod
  def applicants_who_wont_to_budget(temporary_group_id):
    temporary_group = GroupStudents.objects.filter(pk=temporary_group_id).first()

    applicants_wonts_budget = BudgetApplicants.objects.filter(
      temporary_group=temporary_group,
      applicant_wont_to_budget = True
      )
    users = applicants_wonts_budget.values_list('user', flat=True)
    return Profile.objects.filter(user__id__in=users).order_by('-ort_score')



# Класс работает с бюджетными местами
class BudgetPlacesServices:
  # получает сколько процентных мест в группе и сколько абит. хотят на бюджет, возвращает число сколько абит. может вступить
  @staticmethod
  def get_how_math_budgets_place(how_percent, how_many_applicants_no_budget):
    budget_places = round(how_many_applicants_no_budget * (how_percent / 100))
    return budget_places

  # создаем или удаляем объект класса BudgetPlacesServices, вызывая методы(если студент хочет то создаем если нет удаляем)
  @staticmethod
  def toggle_budget_application(user, temporary_group):
    false_or_true = BudgetPlacesServices.is_budget_application_active(user, temporary_group)

    if false_or_true:
      applicant = BudgetApplicants.objects.filter(user=user, temporary_group=temporary_group).first()
      BudgetPlacesServices.delete_budget_application(applicant)
    else: 
      BudgetPlacesServices.create_budget_application(user, temporary_group)

  # получает user и временную группу, возвращает True или False, хочет ли пользователь в бюджет или нет
  @staticmethod
  def is_budget_application_active(user, temporary_group):
    applicant = BudgetApplicants.objects.filter(user=user, temporary_group=temporary_group).first()

    # если пользователь существует то возвращаем значение applicant_wont_to_budget, если нет то False
    return applicant.applicant_wont_to_budget if applicant else False
  
  # получает user, временную группу, и создает объект модели BudgetApplicants
  @staticmethod
  def create_budget_application(user, temporary_group):
    applicant_wont_to_budget = BudgetApplicants.objects.create(
      user = user,
      temporary_group = temporary_group,
      applicant_wont_to_budget = True
    )

  # получаем объект модели BudgetApplicants и удаляем его
  @staticmethod
  def delete_budget_application(applicant):
    applicant.delete()



# Класс: бюджетные абитуриенты вступают в группы(скорее всего после прекращение набора студентов в факультет)
class BudgetApplicantsGoGroupsServices:
  # бюджетные места вступают в группы
  @staticmethod
  def add_state_employees_to_temporary_groups(temporary_group):
    profiles = ProfileServices.applicants_who_wont_to_budget(temporary_group)

    how_many_applicants_no_budget = temporary_group.students_data.count()
    how_percent = temporary_group.budget_place_percent
    budget_places = BudgetPlacesServices.get_how_math_budgets_place(how_percent, how_many_applicants_no_budget)

    for i in budget_places:
      user = profiles[i].user
      ApplicantAdnStudentServices.create_student_data(user, temporary_group, 'Очный')
  
  # вызывает метод который(вступает метод по одному)
  @staticmethod
  def call_method_by_queue(temporary_groups):
    for temporary_group in temporary_groups:
      BudgetApplicantsGoGroupsServices.add_state_employees_to_temporary_groups(temporary_group)



# Класс работает превращением абитуриента в студента
class ApplicantAdnStudentServices:
  # получает профиль, временную группу возвращает достаточно ли у абитуриента ОРТ балла для этой группы
  @staticmethod
  def is_eligible_for_group(profile, temporary_group):
    return profile.ort_score >= temporary_group.min_ort_score
  
  # получаем user чтобы изменить email @apnt.mu на @std.mu
  @staticmethod
  def update_user_email(user):
    user.email = user.email.replace('@apnt.mu', '@std.mu')
    user.save()

  # получаем user, временную группу, форма которая пришла(post), создаем student_data
  @staticmethod
  def create_student_data(user, temporary_group, form_of_training):
    current_year = datetime.datetime.now().year
    # находим в ком годе начался учеба и в коком закончится(гггг.мм.дд)
    start_date = datetime.date(current_year, 9, 1)
    end_date = datetime.date(int(current_year) + int(temporary_group.duration_years) + 1, 6, 5)

    new_student_data = StudentData.objects.create(
    temporary_group = temporary_group,
    user = user,
    start_date = start_date,
    end_date = end_date,
    form_of_training = form_of_training,
    )



# Класс работает с Group
class GroupServices:
  # получает временную группу, создает столько группы сколько нужно
  @staticmethod
  def how_many_groups_we_need(temporary_groups):
    for temporary_group in temporary_groups:
      groups = []
      student_count = temporary_group.students_data.count()
      if student_count > 0:
        for number in range((student_count + 24) // 25):
          new_group = GroupServices.create_group(temporary_group, number)
          GroupServices.transfer_lessons_from_temp_group_to_group(temporary_group, new_group)
          groups.append(new_group)
        GroupServices.redistribute_students_into_groups(temporary_group, groups)

  # получаем временную группу, номер создаем группу
  @staticmethod
  def create_group(temporary_group, number):
    group_code = GroupServices.create_group_code(temporary_group, number)

    new_group = Group.objects.create(
      name = temporary_group.name,  # Копируем имя из GroupStudents
      faculty = temporary_group.faculty,  # Копируем факультет из GroupStudents
      min_ort_score = temporary_group.min_ort_score,  # Минимальный ОРТ
      duration_years = temporary_group.duration_years,  # Длительность обучения
      contract = temporary_group.contract,
      code = group_code,
      curator = None,
    )

    return new_group

  # получаем временную группу и возвращаем часть
  @staticmethod
  def create_group_code(temporary_group, number):
    current_year = datetime.datetime.now().year
    group_code = f"{''.join(word[0].upper() for word in temporary_group.name.split())}-{number + 1}-{current_year % 100}"
    return group_code
  
  # передача уроков из временной группы в основной
  @staticmethod
  def transfer_lessons_from_temp_group_to_group(temporary_group, group):
    # Получаем связанные объекты (уроки) временной группы
    lessons_temporary_group = temporary_group.lessons.all()
    # Связываем все объекты (уроки) с основной группой
    group.lessons.add(*lessons_temporary_group)
    group.save()

  # перераспределяем студентов чтобы они более менее были ровны в каждой группе
  @staticmethod
  def redistribute_students_into_groups(temporary_group, groups):
    students = GroupServices.get_all_students_temporary_group(temporary_group)
    for i, student in enumerate(students):
      group_index = i % len(groups)
      student.group = groups[group_index]
      student.save()
    GroupServices.clear_all_students(temporary_group)

  # получаем временную группу, возвращаем
  @staticmethod
  def get_all_students_temporary_group(temporary_group):
    return temporary_group.students_data.all()
  
  # удаляем связь между временной группой и студентом
  @staticmethod
  def clear_all_students(temporary_group):
    temporary_group.students_data.clear()