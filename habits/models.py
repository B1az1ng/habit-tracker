from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # target – сколько раз нужно выполнить в день
    target_per_day = models.PositiveIntegerField(default=1)
    # сколько уже сделал сегодня
    done_today    = models.PositiveIntegerField(default=0)
    # для подсчёта ежедневных стриков
    last_completed_date = models.DateField(null=True, blank=True)
    streak              = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def mark_done(self):
        today = timezone.localdate()
        # если вчера или ранее последний раз завершали – сбрасываем done_today
        if self.last_completed_date != today:
            self.done_today = 0
        # увеличиваем счётчик сегодня
        if self.done_today < self.target_per_day:
            self.done_today += 1
        # если дошли до target_per_day, отмечаем день как «полностью выполненный»
        if self.done_today == self.target_per_day:
            # если вчера тоже был выполненный день → увеличиваем стрик, иначе =1
            if self.last_completed_date == today - timezone.timedelta(days=1):
                self.streak += 1
            else:
                self.streak = 1
            self.last_completed_date = today
        self.save()

    @property
    def remaining_today(self):
        return max(self.target_per_day - self.done_today, 0)
