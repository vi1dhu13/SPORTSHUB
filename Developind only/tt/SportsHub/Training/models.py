# connect/models.py

from django.db import models
from Members.models import FitnessTrainer
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
from django.db import models


class WorkoutRoutine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    connection = models.ForeignKey(UserTrainerConnection, on_delete=models.CASCADE, related_name='routines')


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class WorkoutExercise(models.Model):
    routine = models.ForeignKey(WorkoutRoutine, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
# models.py
from django.db import models
from Members.models import FitnessTrainer
from users.models import CustomUser

# models.py
from django.db import models
from Members.models import FitnessTrainer,FitnessUser
from users.models import CustomUser

class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE, related_name='created_plans')
    client = models.ForeignKey(FitnessUser, on_delete=models.CASCADE, related_name='assigned_plans', null=True, blank=True)
    name = models.CharField(max_length=255)
    sets = models.ManyToManyField('WorkoutSet', through='WorkoutPlanSet')

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

class WorkoutSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class WorkoutPlanSet(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    workout_set = models.ForeignKey(WorkoutSet, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.workout_plan.name} - {self.workout_set.name}"

from django.db import models

from django.db import models

class Workout(models.Model):
    WORKOUT_TYPES = (
        ('Cardio', 'Cardiovascular'),
        ('Strength', 'Strength Training'),
        ('Core', 'Core Workouts'),
        ('Agility', 'Agility and Coordination'),
        ('MixedModal', 'Mixed Modal'),
        # Add more types as needed
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES, default='Cardio')

    def __str__(self):
        return self.name


from django.db import models
from Members.models import FitnessTrainer
from users.models import CustomUser

class WorkoutCalendar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='calendars')
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    date = models.DateField()
    workouts = models.ManyToManyField('Workout', related_name='calendar_entries')

    def __str__(self):
        return f"{self.user.username}'s Calendar - {self.date}"
