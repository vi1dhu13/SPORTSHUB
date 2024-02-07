
from django.contrib import admin
from .models import UserTrainerConnection, TrainingPlan, Exercise, WorkoutRoutine, Nutrition, NutritionPlan

@admin.register(UserTrainerConnection)
class UserTrainerConnectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'trainer', 'start_date', 'end_date')

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('connection', 'name', 'description', 'hours_per_day', 'days_per_week', 'pace')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'sets', 'reps')

@admin.register(WorkoutRoutine)
class WorkoutRoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creator_user', 'creator_trainer')

@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'calories_per_serving', 'protein_per_serving', 'carbohydrates_per_serving', 'fat_per_serving', 'serving_size', 'quantity')

@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creator_user', 'creator_trainer')
