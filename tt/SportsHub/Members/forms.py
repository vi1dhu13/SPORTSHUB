# forms.py
from django import forms
from .models import TrainerUserConnection,DailyWorkout,WeeklyPlan

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

from django import forms
from .models import EquipmentReservation

class EquipmentReservationForm(forms.ModelForm):
    connected_users = forms.ModelMultipleChoiceField(
        queryset=None,  # You'll set this queryset in the form constructor
        widget=forms.Select,  # Use SelectMultiple widget for a dropdown box
        required=False,  # Set to False if you want to make it optional
    )
    

    class Meta:
        model = EquipmentReservation
        fields = ['trainer', 'equipment', 'timeslot', 'date']

    def __init__(self, *args, **kwargs):
        connected_users_queryset = kwargs.pop('connected_users_queryset', None)
        super(EquipmentReservationForm, self).__init__(*args, **kwargs)

        # Set the queryset for connected_users field
        if connected_users_queryset is not None:
            self.fields['connected_users'].queryset = connected_users_queryset




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

from django import forms

class WeeklyPlanForm(forms.ModelForm):
    class Meta:
        model = WeeklyPlan
        fields = ['plan_name', 'start_date', 'end_date']

class DailyWorkoutFormSet(forms.ModelForm):
    class Meta:
        model = DailyWorkout
        fields = ['day_of_week', 'workout_details']
from django import forms
from .models import WeeklyFitnessPlan

class WeeklyFitnessPlanForm(forms.ModelForm):
    class Meta:
        model = WeeklyFitnessPlan
        fields = ['fitness_user', 'start_date', 'end_date', 'day1details', 'day2details', 'day3details', 'day4details', 'day5details', 'day6details', 'day7details']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define which fields need special attributes
        custom_attrs = {
            'fitness_user': {'class': 'form-control'},
            'start_date': {'class': 'form-control datepicker'},
            'end_date': {'class': 'form-control datepicker'},
        }

        # Apply custom attributes to form fields
        for field_name, attrs in custom_attrs.items():
            self.fields[field_name].widget.attrs.update(attrs)

        # Apply custom CSS classes and textarea attributes to day details fields
        textarea_attrs = {'class': 'form-control expandable-textarea', 'rows': 1}
        day_details_fields = ['day1details', 'day2details', 'day3details', 'day4details', 'day5details', 'day6details', 'day7details']
        for field_name in day_details_fields:
            self.fields[field_name].widget = forms.Textarea(attrs=textarea_attrs)
