

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
    def __str__(self):
        return self.user.username
         
class FitnessTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    experience = models.IntegerField()
    certification = models.CharField(max_length=255, null=True, blank=True)
    training_goal = models.CharField(max_length=255)
    certification_link = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    # Add other fields specific to FitnessTrainer
    def __str__(self):
        return self.user.username

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
from .models import FitnessUser, FitnessTrainer

class TrainingPlan(models.Model):
    plan_name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()  # Duration in days, weeks, etc.
    created_by_trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.plan_name


from django.db import models
from .models import FitnessUser, TrainingPlan

class TrainingPlanAssignment(models.Model):
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Assignment for {self.user.user.username}"

from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

from django.db import models

class TimeSlot(models.Model):
    slot_number = models.PositiveIntegerField(unique=True,default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Slot {self.slot_number}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

from django.db import models
from django.utils import timezone

class EquipmentReservation(models.Model):
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE,default=1)
    fitness_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE,default=1)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,default=1)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Reservation for {self.equipment.name} on {self.date} by {self.fitness_user.user.username}"
