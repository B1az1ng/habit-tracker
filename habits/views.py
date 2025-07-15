from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.utils import timezone
from datetime import date
from django.db import models

from .models import Habit
from .forms import HabitForm

def home(request):
    return redirect('habit_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('habit_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def habit_list(request):
    # Добавление новой
    if request.method == 'POST' and 'add_habit' in request.POST:
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()

    habits = Habit.objects.filter(user=request.user)
    # глобальный стрик — минимум по всем привычкам за последние дни подряд?
    # тут простой вариант: максимум из стриков привычек
    global_streak = habits.aggregate(ms=models.Max('streak'))['ms'] or 0

    return render(request, 'habit_list.html', {
        'habits': habits,
        'form': form,
        'global_streak': global_streak,
    })

@login_required
def complete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    # Используем уже реализованный метод
    habit.mark_done()
    habit.save()

    return redirect('habit_list')
@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habit_list')
