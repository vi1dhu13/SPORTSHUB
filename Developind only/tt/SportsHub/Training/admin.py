from django.contrib import admin
# your_app/admin.py
from django.contrib import admin
from .models import WorkoutSet, WorkoutPlan, WorkoutPlanSet

class WorkoutPlanSetInline(admin.TabularInline):
    model = WorkoutPlanSet
    extra = 1

@admin.register(WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'client')
    inlines = [WorkoutPlanSetInline]

@admin.register(WorkoutPlanSet)
class WorkoutPlanSetAdmin(admin.ModelAdmin):
    list_display = ('workout_plan', 'workout_set', 'order')

