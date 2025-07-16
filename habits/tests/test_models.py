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
        # 1→2→3 отметки, completion только на третьей
        for i in range(3):
            self.habit.mark_done()
            self.habit.refresh_from_db()
            self.assertEqual(self.habit.done_today, i+1)
            self.assertEqual(self.habit.is_completed, (i+1) >= 3)

    def test_unmark_done_decrements_and_unsets(self):
        # доводим до completion
        for _ in range(3):
            self.habit.mark_done()
        self.habit.refresh_from_db()
        self.assertTrue(self.habit.is_completed)

        # откатываем одну отметку
        self.habit.unmark_done()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.done_today, 2)
        self.assertFalse(self.habit.is_completed)

    def test_mark_done_resets_on_new_day(self):
        # первый день: делаем 2 отметки
        for _ in range(2):
            self.habit.mark_done()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.done_today, 2)

        # эмулируем следующий день
        today = timezone.localdate()
        yesterday = today - timezone.timedelta(days=1)
        # вручную правим дату последнего выполнения
        Habit.objects.filter(pk=self.habit.pk).update(last_completed_date=yesterday)
        # теперь mark_done() должен сбросить done_today и поставить 1
        self.habit.mark_done()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.done_today, 1)
