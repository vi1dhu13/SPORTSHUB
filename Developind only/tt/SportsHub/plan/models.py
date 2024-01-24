from django.db import models

# Create your models here.
from django.db import models
 
# Create your models here.
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 
    class Meta:  
        db_table = "tblevents"


# models.py
from django.db import models
from Members.models import FitnessTrainer, FitnessUser
from Training.models import Workout

class DailyEvents(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    fitness_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    workouts = models.ManyToManyField(Workout)

    def __str__(self):
        return self.name


class WorkoutPlanDetail(models.Model):
    workout_plan = models.ForeignKey('WorkoutPlan', on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.workout_plan.name} - {self.workout.name} - Order: {self.order}"

class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    workouts = models.ManyToManyField(Workout, through='WorkoutPlanDetail')
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer.user.username}'s Plan for {self.user.user.username}: {self.name}"