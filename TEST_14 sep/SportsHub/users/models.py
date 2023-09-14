from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20)  # Define roles (e.g., "FitnessUser", "FitnessTrainer", "SportsTrainer")
    description = models.TextField(blank=True, null=True)  # Add the description field

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    
from django.db import models
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name




class CommonChoice(models.Model):
    FITNESS_GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('calisthenics', 'Calisthenics'),
        ('crossfit', 'Crossfit'),
        ('bodybuilding', 'Bodybuilding'),
    ]

    name = models.CharField(max_length=255, choices=FITNESS_GOAL_CHOICES)
    choice_type = models.CharField(
        max_length=25,  # Updated max_length to accommodate the longest choice
        choices=[('fitness_goal', 'Fitness Goal'), ('trainer_specialization', 'Trainer Specialization')],
    )

    def __str__(self):
        return self.get_name_display()

    
from django.db import models
from .models import CustomUser,CommonChoice


class RoleApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    specialization_details = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    # New fields for fitness application
    fitness_goal = models.ForeignKey(CommonChoice, on_delete=models.CASCADE, blank=True, null=True, related_name="fitness_applications")
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    
    experience = models.IntegerField()
   
    # Other fields...

    certification = models.CharField(max_length=255, default="No Certification")
    certification_link = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    
    

    def __str__(self):
        return f"{self.user.username} - {self.role.name} Application"