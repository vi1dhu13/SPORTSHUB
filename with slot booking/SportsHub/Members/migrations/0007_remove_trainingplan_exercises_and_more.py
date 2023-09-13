# Generated by Django 4.2.4 on 2023-09-09 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0006_trainingplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingplan',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='trainingplan',
            name='trainer',
        ),
        migrations.RemoveField(
            model_name='trainingplan',
            name='user',
        ),
        migrations.AlterField(
            model_name='trainingplan',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
