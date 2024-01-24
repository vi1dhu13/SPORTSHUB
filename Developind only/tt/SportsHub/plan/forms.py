

from django import forms
from .models import Workout, FitnessUser


from django import forms
from .models import DailyEvents
from Members.models import FitnessUser
from Training.models import Workout

from django import forms
from .models import DailyEvents
from Members.models import FitnessUser
from Training.models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = DailyEvents
        fields = ['start', 'end', 'workouts', 'fitness_user']  # Adjust the fields accordingly

    start_date = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    workouts = forms.ModelMultipleChoiceField(
        queryset=Workout.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    fitness_user = forms.ModelChoiceField(queryset=FitnessUser.objects.all(), to_field_name='id')







