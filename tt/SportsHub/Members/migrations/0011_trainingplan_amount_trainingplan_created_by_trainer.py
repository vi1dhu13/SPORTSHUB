# Generated by Django 4.2.4 on 2023-09-11 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0010_fitnesstrainer_certification_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingplan',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='trainingplan',
            name='created_by_trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Members.fitnesstrainer'),
        ),
    ]
