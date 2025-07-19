from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from habits.models import Habit

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pass')
        self.habit = Habit.objects.create(
            user=self.user,
            name='Meditate',
            target_per_day=3,
        )

    def test_mark_done_increments_and_completes(self):
        # Проверяем: done_today растёт 1→2→3, и is_completed=True только на третьей отметке
        for i in range(3):
            self.habit.mark_done()
            self.habit.refresh_from_db()
            self.assertEqual(self.habit.done_today, i+1)
            self.assertEqual(self.habit.is_completed, (i+1) >= 3)

    def test_unmark_done_decrements_and_unsets(self):
        # Доводим до completion
        for _ in range(3):
            self.habit.mark_done()
        self.habit.refresh_from_db()
        self.assertTrue(self.habit.is_completed)

        # Откатываем одну отметку — done_today станет 2, is_completed=False
        self.habit.unmark_done()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.done_today, 2)
        self.assertFalse(self.habit.is_completed)

    def test_mark_done_resets_on_new_day(self):
        # Первый день: делаем 2 отметки
        for _ in range(2):
            self.habit.mark_done()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.done_today, 2)

        # Эмулируем следующий день
        yesterday = timezone.localdate() - timezone.timedelta(days=1)
        Habit.objects.filter(pk=self.habit.pk).update(last_completed_date=yesterday)

        # Теперь mark_done() должен сбросить счётчик и выставить done_today=1
        self.habit.mark_done()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.done_today, 1)