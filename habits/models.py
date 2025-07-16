# habits/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    name                = models.CharField(max_length=100)
    target_per_day      = models.PositiveIntegerField(default=1)
    done_today          = models.PositiveIntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)
    streak              = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def mark_done(self):
        today = timezone.localdate()

        # если мы в новый день — сбрасываем счётчик
        if self.last_completed_date != today:
            self.done_today = 0

        # фиксируем дату (чтобы в следующий раз не сбросило)
        self.last_completed_date = today

        # увеличиваем счётчик до target_per_day
        if self.done_today < self.target_per_day:
            self.done_today += 1

        # если сегодня уже полностью отработали привычку — считаем стрим
        if self.done_today >= self.target_per_day:
            # предыдущий день подряд?
            yesterday = today - timezone.timedelta(days=1)
            if Habit.objects.filter(user=self.user, last_completed_date=yesterday,
                                    done_today__gte=models.F('target_per_day')).exists():
                self.streak += 1
            else:
                self.streak = 1

        self.save()

    def unmark_done(self):
        """
        Откат одного выполнения за сегодня.
        Если мы в тот же день, уменьшаем done_today, и сбрасываем is_completed,
        если цель не достигнута.
        """
        today = timezone.localdate()
        # работаем только в тот же день, когда ставили отметку
        if self.last_completed_date == today and self.done_today > 0:
            self.done_today -= 1
            # если теперь стало меньше target_per_day — сбрасываем флаг
            if self.done_today < self.target_per_day:
                self.is_completed = False
            self.save()

    @property
    def remaining_today(self):
        return max(self.target_per_day - self.done_today, 0)
    
class HabitRecord(models.Model):
    habit     = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='records')
    date      = models.DateField()
    done      = models.PositiveIntegerField()
    completed = models.BooleanField()

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']
