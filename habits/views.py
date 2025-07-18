from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.db.models import Max

from .models import Habit
from .models import Profile
from .forms import HabitForm
from .forms import ProfileForm


def home(request):
    return redirect('habit_list')

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


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
    # Добавление новой привычки при любом POST
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()

    habits = Habit.objects.filter(user=request.user)
    global_streak = habits.aggregate(ms=Max('streak'))['ms'] or 0

    return render(request, 'habit_list.html', {
        'habits': habits,
        'form': form,
        'global_streak': global_streak,
    })


@login_required
def complete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.mark_done()
    return redirect('habit_list')


@login_required
def uncomplete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.unmark_done()
    return redirect('habit_list')


@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habit_list')