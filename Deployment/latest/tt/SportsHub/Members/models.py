


from django.db import models
from users.models import CustomUser



class FitnessUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=255)
    height = models.FloatField()
    weight = models.FloatField()
    medical_conditions_text = models.TextField(blank=True, null=True)
    medical_conditions_pdf = models.FileField(upload_to='medical_conditions_pdfs/', blank=True, null=True)

    def __str__(self):
        return self.user.username

         
class FitnessTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    experience = models.IntegerField()
    certification = models.CharField(max_length=255, null=True, blank=True)
    training_goal = models.CharField(max_length=255)
    certification_link = models.CharField(max_length=255, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
  
    def __str__(self):
        return self.user.username

class SportsTrainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255,null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)




from django.db import models

class TrainerUserConnection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'), 
        ('approved', 'Approved'),  
        ('rejected', 'Rejected'),  
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
    duration = models.IntegerField()  
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
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)  
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.plan_name

class DailyWorkout(models.Model):
    weekly_plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE)
    day_of_week = models.PositiveIntegerField() 
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

    trainer = models.ForeignKey('FitnessTrainer', on_delete=models.CASCADE) 
    fitness_user = models.ForeignKey('FitnessUser', on_delete=models.CASCADE) 
    day1details = models.TextField(null=True, blank=True)
    day2details = models.TextField(null=True, blank=True)
    day3details = models.TextField(null=True, blank=True)
    day4details = models.TextField(null=True, blank=True)
    day5details = models.TextField(null=True, blank=True)
    day6details = models.TextField(null=True, blank=True)
    day7details = models.TextField(null=True, blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.end_date:
            
            self.end_date = self.start_date + timedelta(days=6)
        super().save(*args, **kwargs)

 

    def __str__(self):
        return f"Weekly Fitness Plan for {self.fitness_user.user.username} by {self.trainer.user.username}"



from django.db import models

class GymSlot(models.Model):
  
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



