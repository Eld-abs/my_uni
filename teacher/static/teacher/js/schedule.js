// это функция помогает видеть элементы при нажатии
function showSchedule(day) {
  // проверяется каждый элемент с классом schedule, и каждый элемент становаится не видемым
  const schedules = document.querySelectorAll('.schedule');
  schedules.forEach(schedule => {
    schedule.classList.remove('active');
  });
  // когда мы кликаем мы доем active к определённому элементу, а позже делаем его видемым
  const activeSchedule = document.getElementById(day);
  activeSchedule.classList.add('active');
}