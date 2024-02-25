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
       widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: white;'})
  # Add a class for styling
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Add a class and rows for styling
    )

    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),  # Add a class for styling
    )



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


from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['trainer', 'fitness_user', 'slot', 'reservation_date']  # Include the fields you want in the form
        widgets = {
        'reservation_date': forms.DateInput(attrs={'class': 'datepicker'}),
    }
        

# forms.py

