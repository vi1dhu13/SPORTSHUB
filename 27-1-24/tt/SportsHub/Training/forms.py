# Training/forms.py

from django import forms
from .models import UserTrainerConnection,WorkoutRoutine

class UserTrainerConnectionForm(forms.ModelForm):
    class Meta:
        model = UserTrainerConnection
        fields = ['trainer', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# forms.py
# forms.py
from django import forms
from .models import WorkoutRoutine,Exercise

class WorkoutRoutineForm(forms.ModelForm):
    class Meta:
        model = WorkoutRoutine
        fields = ['name', 'description', 'exercises','creator_user']

    def __init__(self, *args, trainer=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if trainer:
            # Limit the choices for creator_user to the trainer's connected users
            self.fields['creator_user'].queryset = trainer.connected_users.all()

            # Set the widget for exercises to CheckboxSelectMultiple
            self.fields['exercises'].widget = forms.CheckboxSelectMultiple()

    # Override the default label for the exercises field
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),  # Provide the queryset for Exercise model
        widget=forms.CheckboxSelectMultiple,
        label='Exercises'
    )
