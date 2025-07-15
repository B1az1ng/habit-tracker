from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'target_per_day']
