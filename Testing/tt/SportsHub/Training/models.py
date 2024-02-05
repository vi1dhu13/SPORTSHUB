
from django.db import models
from Members.models import FitnessTrainer,FitnessUser
from users.models import CustomUser

class UserTrainerConnection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='connections')
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE, related_name='connections')
    start_date = models.DateField()
    end_date = models.DateField()
    # Add other fields related to the connection

    def __str__(self):
        return f"{self.user.username} - {self.trainer.user.username} Connection"

class TrainingPlan(models.Model):
    connection = models.ForeignKey(UserTrainerConnection, on_delete=models.CASCADE, related_name='training_plans')
    name = models.CharField(max_length=255)
    description = models.TextField()
    hours_per_day = models.PositiveIntegerField()
    days_per_week = models.PositiveIntegerField()
    pace = models.CharField(max_length=255)
    # Add other fields specific to training plans

    def __str__(self):
        return self.name


# models.py


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class WorkoutRoutine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exercises = models.ManyToManyField(Exercise, related_name='workout_routines')
    creator_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE, null=True, blank=True)
    creator_trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Nutrition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    calories_per_serving = models.PositiveIntegerField()
    protein_per_serving = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates_per_serving = models.DecimalField(max_digits=5, decimal_places=2)
    fat_per_serving = models.DecimalField(max_digits=5, decimal_places=2)
    serving_size = models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models
from .models import FitnessUser, FitnessTrainer, Nutrition
class NutritionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    items = models.ManyToManyField(Nutrition, related_name='nutrition_plans')
    creator_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE, null=True, blank=True)
    creator_trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
from django.db import models




# models.py
from django.db import models
from django.conf import settings

class MedicalOverview(models.Model):
    user = models.OneToOneField(FitnessUser, on_delete=models.CASCADE, related_name='medical_overview')
    conditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical Overview for {self.user.username}"
