# Generated by Django 5.0.1 on 2024-01-27 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0031_remove_workoutregimen_connection_and_more'),
        ('Training', '0011_remove_workoutcalendar_workouts_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('calories', models.PositiveIntegerField()),
                ('protein', models.DecimalField(decimal_places=2, max_digits=5)),
                ('carbohydrates', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('additional_info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('creator_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Members.fitnesstrainer')),
                ('creator_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Members.fitnessuser')),
                ('items', models.ManyToManyField(related_name='nutrition_plans', to='Training.nutrition')),
            ],
        ),
    ]
