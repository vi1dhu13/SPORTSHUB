from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FitnessUser, FitnessTrainer, SportsTrainer
from django.contrib import admin
from .models import TrainerUserConnection

@admin.register(FitnessUser)
class FitnessUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'fitness_goal', 'height', 'weight')
    # Add any other desired admin options

@admin.register(FitnessTrainer)
class FitnessTrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'certification', 'training_goal')
    # Add any other desired admin options

@admin.register(SportsTrainer)
class SportsTrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    # Add any other desired admin options


@admin.register(TrainerUserConnection)
class TrainerUserConnectionAdmin(admin.ModelAdmin):
    list_display = ('fitness_trainer', 'fitness_user', 'status')
    list_filter = ('status',)
    search_fields = ('fitness_trainer__user__username', 'fitness_user__user__username')
