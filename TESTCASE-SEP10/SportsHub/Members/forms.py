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




class TrainingPlanForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=None,  # We will set this queryset dynamically in the view
        label='Select a User',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    plan_name = forms.CharField(max_length=255, label='Plan Name')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    duration = forms.IntegerField(label='Duration (in days, weeks, etc.)')
