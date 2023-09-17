# Generated by Django 4.2.4 on 2023-09-11 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0014_remove_exerciseset_exercise_remove_exerciseset_plan_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=255)),
                ('sets', models.PositiveIntegerField()),
                ('repetitions', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Members.fitnessuser')),
                ('exercise_sets', models.ManyToManyField(to='Members.exerciseset')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Members.fitnesstrainer')),
            ],
        ),
    ]
