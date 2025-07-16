# habits/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.utils import timezone


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Сколько раз нужно выполнить сегодня
    target_per_day = models.PositiveIntegerField(default=1)
    # Сколько уже выполнено сегодня
    done_today = models.PositiveIntegerField(default=0)
    # Дата последнего выполнения
    last_completed_date = models.DateField(null=True, blank=True)
    # Текущий стрик — дней подряд, когда цель достигалась
    streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_completed(self):
        """
        True, если done_today >= target_per_day
        """
        return self.done_today >= self.target_per_day

    @property
    def remaining_today(self):
        """
        Сколько раз ещё осталось выполнить сегодня
        """
        return max(self.target_per_day - self.done_today, 0)

    def mark_done(self):
        """
        Отметить ещё одно выполнение сегодня.
        Сбрасывает счётчик при смене дня, обновляет стрик.
        """
        # Обновим поля из базы, чтобы корректно обработать смену дня
        self.refresh_from_db(fields=['last_completed_date', 'done_today', 'streak'])
        today = timezone.localdate()

        # Если вчерашняя дата отличается от сегодня — начинаем новый день
        if self.last_completed_date != today:
            self.done_today = 0
            self.last_completed_date = today

        # Увеличиваем счётчик до target_per_day
        if self.done_today < self.target_per_day:
            self.done_today += 1

        # Если сегодня уже выполнили цель — пересчитываем стрик
        if self.done_today >= self.target_per_day:
            yesterday = today - timezone.timedelta(days=1)
            # Проверяем, был ли вчера стрик
            if Habit.objects.filter(
                user=self.user,
                last_completed_date=yesterday,
                done_today__gte=F('target_per_day')
            ).exists():
                self.streak += 1
            else:
                self.streak = 1

        # Сохраняем изменения
        self.save()

    def unmark_done(self):
        """
        Откат одного выполнения за сегодня.
        Уменьшает done_today, не трогает стрик и дату.
        """
        today = timezone.localdate()
        if self.last_completed_date == today and self.done_today > 0:
            self.done_today -= 1
            # Просто сохраняем — is_completed это свойство, авто‑сбросит статус
            self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',    # файлы будут сохраняться в MEDIA_ROOT/avatars/
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"


class HabitRecord(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='records'
    )
    date = models.DateField()
    # сколько раз сделал в этот день
    done = models.PositiveIntegerField()
    # достиг цели в этот день?
    completed = models.BooleanField()

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']
