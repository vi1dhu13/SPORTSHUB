

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
    certification_link = models.CharField(max_length=255, blank=True, null=True)  # Add this field
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




# # Define a model for exercises
# class Exercise(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# # Define a model for workout days, which can contain multiple exercises
# class WorkoutDay(models.Model):
#     day_number = models.PositiveIntegerField()
#     exercises = models.ManyToManyField(Exercise, through='ExerciseSet')

#     def __str__(self):
#         return f"Day {self.day_number}"

# # Define a model to represent sets and repetitions for each exercise on a workout day
# class ExerciseSet(models.Model):
#     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
#     workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
#     sets = models.PositiveIntegerField()
#     repetitions = models.PositiveIntegerField()

#     def __str__(self):
#         return f"Set {self.sets}, Repetitions {self.repetitions} - {self.exercise.name}"

# # Define a model for workout plans, which consist of workout days
# class WorkoutPlan(models.Model):
#     trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
#     client = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
#     week_number = models.PositiveIntegerField()
#     date = models.DateField()
#     workout_days = models.ManyToManyField(WorkoutDay)

#     def __str__(self):
#         return f"Week {self.week_number} Workout Plan for {self.client.user.username}"

# # Define a model to represent workout plan assignments
# class WorkoutPlanAssignment(models.Model):
#     user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
#     plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
#     assigned_by = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
#     assigned_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Assignment for {self.user.user.username}"
