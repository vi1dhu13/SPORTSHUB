# Training/forms.py

from django import forms
from .models import UserTrainerConnection

class UserTrainerConnectionForm(forms.ModelForm):
    class Meta:
        model = UserTrainerConnection
        fields = ['trainer', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# forms.py
from datetime import date
from django import forms
from .models import WorkoutRoutine

class WorkoutRoutineForm(forms.ModelForm):
    class Meta:
        model = WorkoutRoutine
        fields = ['name', 'description', 'connection']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the connections based on the current user
        self.fields['connection'].queryset = UserTrainerConnection.objects.filter(user=user, end_date__gte=date.today())
