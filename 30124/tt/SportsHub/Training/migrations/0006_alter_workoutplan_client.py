# Generated by Django 5.0.1 on 2024-01-16 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0029_equipment_timeslot_equipmentreservation'),
        ('Training', '0005_alter_usertrainerconnection_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutplan',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_plans', to='Members.fitnessuser'),
        ),
    ]