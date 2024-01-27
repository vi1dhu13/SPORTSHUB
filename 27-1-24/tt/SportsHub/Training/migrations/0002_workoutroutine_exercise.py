# Generated by Django 5.0.1 on 2024-01-12 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutRoutine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='Training.usertrainerconnection')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField()),
                ('routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Training.workoutroutine')),
            ],
        ),
    ]
