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
from .models import WorkoutRoutine, UserTrainerConnection

class WorkoutRoutineForm(forms.ModelForm):
    class Meta:
        model = WorkoutRoutine
        fields = ['name', 'description', 'connection']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the connections based on the current user
        self.fields['connection'].queryset = UserTrainerConnection.objects.filter(user=user, end_date__gte=date.today())

        # Add some styling to the form fields
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter routine name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter routine description'})
        self.fields['connection'].widget.attrs.update({'class': 'form-control'})


# forms.py
# forms.py
from django import forms
from .models import WorkoutPlan

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'sets']


