

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
    certification_link = models.CharField(max_length=255, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)# Add this field
    # Add other fields specific to FitnessTrainer
    def __str__(self):
        return self.user.username

class SportsTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
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

class WeeklyPlan(models.Model):
    trainer_connection = models.ForeignKey(TrainerUserConnection, on_delete=models.CASCADE)
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)  # User who receives the plan
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.plan_name

class DailyWorkout(models.Model):
    weekly_plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE)
    day_of_week = models.PositiveIntegerField()  # 1 for Monday, 2 for Tuesday, etc.
    workout_details = models.TextField()

    def __str__(self):
        return f"{self.weekly_plan.plan_name} - Day {self.day_of_week}"
from django.db import models
from datetime import date, timedelta
from .models import TrainerUserConnection

class WeeklyFitnessPlan(models.Model):
    DAYS_OF_WEEK = (
        ('day1', 'Day 1'),
        ('day2', 'Day 2'),
        ('day3', 'Day 3'),
        ('day4', 'Day 4'),
        ('day5', 'Day 5'),
        ('day6', 'Day 6'),
        ('day7', 'Day 7'),
    )

    trainer = models.ForeignKey('FitnessTrainer', on_delete=models.CASCADE)  # Replace 'YourApp.FitnessTrainer' with your actual FitnessTrainer model
    fitness_user = models.ForeignKey('FitnessUser', on_delete=models.CASCADE) 
    day1details = models.TextField(null=True, blank=True)
    day2details = models.TextField(null=True, blank=True)
    day3details = models.TextField(null=True, blank=True)
    day4details = models.TextField(null=True, blank=True)
    day5details = models.TextField(null=True, blank=True)
    day6details = models.TextField(null=True, blank=True)
    day7details = models.TextField(null=True, blank=True)# Replace 'YourApp.FitnessUser' with your actual FitnessUser model
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)  # Allow null and blank for now

    def save(self, *args, **kwargs):
        if not self.end_date:
            # Calculate the end date based on the start date
            self.end_date = self.start_date + timedelta(days=6)
        super().save(*args, **kwargs)

 

    def __str__(self):
        return f"Weekly Fitness Plan for {self.fitness_user.user.username} by {self.trainer.user.username}"



from django.db import models

class GymSlot(models.Model):
    """
    Model to represent gym time slots available for reservation.
    """
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=6)

    def __str__(self):
        return f" {self.start_time} - {self.end_time}"

class Reservation(models.Model):
    """
    Model to represent gym slot reservations.
    """
    trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    fitness_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    slot = models.ForeignKey(GymSlot, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.fitness_user} with {self.trainer} on {self.reservation_date} {self.slot.start_time} - {self.slot.end_time}"
