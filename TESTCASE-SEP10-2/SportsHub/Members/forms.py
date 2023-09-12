# forms.py
from django import forms
from .models import TrainerUserConnection

class TrainerUserConnectionForm(forms.ModelForm):
    class Meta:
        model = TrainerUserConnection
        fields = ['fitness_user', 'fitness_trainer', 'status']
        widgets = {
            'fitness_user': forms.HiddenInput(),  # Hide the user field, set it in the view
            'status': forms.HiddenInput(),  # Hide the status field, set it in the view
        }

# forms.py
from django import forms
from .models import FitnessTrainer

class TrainerSelectionForm(forms.Form):
    selected_trainer = forms.ModelChoiceField(
        queryset=FitnessTrainer.objects.all(),
        label='Select a Trainer',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )




# class TrainingPlanForm(forms.Form):
#     user = forms.ModelChoiceField(
#         queryset=None,  # We will set this queryset dynamically in the view
#         label='Select a User',
#         widget=forms.Select(attrs={'class': 'form-control'}),
#     )
#     plan_name = forms.CharField(max_length=255, label='Plan Name')
#     description = forms.CharField(widget=forms.Textarea, label='Description')
#     duration = forms.IntegerField(label='Duration (in days, weeks, etc.)')
from django import forms
from .models import TrainingPlan

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['plan_name', 'description', 'duration', 'amount']  # Exclude 'created_by_trainer'

    duration = forms.IntegerField(
        label='Duration (in Months.)',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),  # Add a class for styling
    )

    plan_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),  # Add a class for styling
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Add a class and rows for styling
    )

    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),  # Add a class for styling
    )

# from django import forms
# from .models import FitnessUser

# class WeeklyWorkoutPlanForm(forms.Form):
#     client = forms.ModelChoiceField(
#         queryset=FitnessUser.objects.none(),
#         required=True,
#         empty_label="Select a client"
#     )
#     week_number = forms.IntegerField(required=True)
#     start_date = forms.DateField(required=True)
#     trainer = forms.ModelChoiceField(
#         queryset=FitnessUser.objects.none(),
#         widget=forms.HiddenInput()
#     )

#     def __init__(self, *args, trainer=None, **kwargs):
#         super().__init__(*args, **kwargs)

#         if trainer:
#             self.fields['trainer'].queryset = FitnessUser.objects.filter(pk=trainer.pk)
#             self.fields['client'].queryset = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)

