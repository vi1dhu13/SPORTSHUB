# Generated by Django 4.2.4 on 2023-09-11 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0017_exercise_exerciseset_workoutday_workoutplan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciseset',
            name='exercise',
        ),
        migrations.RemoveField(
            model_name='exerciseset',
            name='workout_day',
        ),
        migrations.RemoveField(
            model_name='workoutday',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='client',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='trainer',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='workout_days',
        ),
        migrations.RemoveField(
            model_name='workoutplanassignment',
            name='assigned_by',
        ),
        migrations.RemoveField(
            model_name='workoutplanassignment',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='workoutplanassignment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Exercise',
        ),
        migrations.DeleteModel(
            name='ExerciseSet',
        ),
        migrations.DeleteModel(
            name='WorkoutDay',
        ),
        migrations.DeleteModel(
            name='WorkoutPlan',
        ),
        migrations.DeleteModel(
            name='WorkoutPlanAssignment',
        ),
    ]
