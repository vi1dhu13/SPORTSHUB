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

# forms.py

# forms.py

from django import forms
from .models import NutritionPlan, Nutrition
from .models import FitnessUser
# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import NutritionPlan, Nutrition, FitnessUser

class NutritionPlanAssignmentForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['name', 'description', 'items']

    def __init__(self, *args, trainer=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.trainer = trainer
        self.user = user

        # Set up checkboxes for selecting multiple nutrition items
        self.fields['items'].widget = forms.CheckboxSelectMultiple()

        # Print the queryset to the console for debugging
        print(Nutrition.objects.all())
        self.fields['items'].queryset = Nutrition.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.trainer:
            instance.creator_trainer = self.trainer

        if self.user:
            # Fetch the FitnessUser instance associated with the CustomUser instance
            fitness_user = FitnessUser.objects.get(user=self.user)
            instance.creator_user = fitness_user

        if commit:
            try:
                instance.full_clean()  # Validate model fields
                instance.save()
            except ValidationError as e:
                print("Validation Error:", e)

        return instance


# forms.py
from django import forms
from .models import MedicalOverview

class MedicalOverviewForm(forms.ModelForm):
    class Meta:
        model = MedicalOverview
        fields = ['conditions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional customization for the form, if needed
