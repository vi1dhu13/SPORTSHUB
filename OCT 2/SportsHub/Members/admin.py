from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FitnessUser, FitnessTrainer, SportsTrainer
from django.contrib import admin
from .models import TrainerUserConnection,TrainingPlan,TrainingPlanAssignment

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

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'duration')
    search_fields = ('plan_name', 'description')




@admin.register(TrainingPlanAssignment)
class TrainingPlanAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'assigned_by', 'assigned_date', 'is_accepted')
    list_filter = ('is_accepted', 'assigned_date')
    search_fields = ('user__user__username', 'plan__plan_name', 'assigned_by__user__username')


# Register your models here
from django.contrib import admin
from .models import GymSlot, Reservation

@admin.register(GymSlot)
class GymSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'capacity')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'fitness_user', 'slot', 'reservation_date', 'reservation_time')
