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

        
from django.db import models
from Members.models import FitnessTrainer, FitnessUser
from Training.models import Workout

class dailyEvents(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    fitness_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    workouts = models.ManyToManyField(Workout)

    def __str__(self):
        return self.name
