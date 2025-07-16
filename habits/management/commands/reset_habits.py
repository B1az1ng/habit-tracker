from django.core.management.base import BaseCommand
from django.utils import timezone
from habits.models import Habit, HabitRecord

class Command(BaseCommand):
    help = "Save yesterday's stats and reset today's counters for all habits"

    def handle(self, *args, **options):
        today = timezone.localdate()
        for habit in Habit.objects.all():
            yesterday = today - timezone.timedelta(days=1)
            if not HabitRecord.objects.filter(habit=habit, date=yesterday).exists():
                done = getattr(habit, 'done_today', 0)
                completed = done >= habit.target_per_day
                HabitRecord.objects.create(
                    habit=habit,
                    date=yesterday,
                    done=done,
                    completed=completed,
                )
            habit.done_today   = 0
            habit.is_completed = False
            habit.save()
        self.stdout.write(f"Habits reset and history saved for {today}")
