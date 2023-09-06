

# Create your models here.
from django.db import models
from users.models import CustomUser
# members/models.py



class FitnessUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=255)
    height = models.FloatField()
    weight = models.FloatField()
    # Add other fields specific to FitnessUser

class FitnessTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    experience = models.IntegerField()
    certification = models.CharField(max_length=255)
    training_goal = models.CharField(max_length=255)
    certification_link = models.URLField(max_length=255, blank=True, null=True)  # Added certification_link field
    # Add other fields specific to FitnessTrainer

    def __str__(self):
        return self.user.username


class SportsTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    # Add other fields specific to SportsTrainer


