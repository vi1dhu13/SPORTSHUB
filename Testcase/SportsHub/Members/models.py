

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
    certification = models.CharField(max_length=255, null=True, blank=True)
    training_goal = models.CharField(max_length=255)
    # Add other fields specific to FitnessTrainer

class SportsTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    # Add other fields specific to SportsTrainer




from django.db import models

class TrainerUserConnection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),  # Request is pending approval
        ('approved', 'Approved'),  # Request has been approved
        ('rejected', 'Rejected'),  # Request has been rejected
    )

    fitness_trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    fitness_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Connection between {self.fitness_user.user.username} and {self.fitness_trainer.user.username}"



from django.db import models

class TrainingPlan(models.Model):
    plan_name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()  # Duration in days, weeks, etc.

    def __str__(self):
        return self.plan_name

