# Generated by Django 4.2.4 on 2023-09-09 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0007_remove_trainingplan_exercises_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnesstrainer',
            name='certification',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
