# Generated by Django 4.2.5 on 2023-10-04 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0028_alter_gymslot_capacity'),
        ('SportsHubApp', '0008_reservation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='Reservation',
        ),
        migrations.AddField(
            model_name='payment',
            name='TrainingPlanAssignment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Members.trainingplanassignment'),
        ),
        migrations.AddField(
            model_name='payment',
            name='reservation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SportsHubApp.reservation'),
        ),
    ]