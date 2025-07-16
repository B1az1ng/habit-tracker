from django import forms
from .models import Habit
from .models import Profile

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'target_per_day']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
