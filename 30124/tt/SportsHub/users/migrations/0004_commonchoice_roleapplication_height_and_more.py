# Generated by Django 4.2.4 on 2023-09-02 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_roleapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('weight_loss', 'Weight Loss'), ('weight_gain', 'Weight Gain'), ('calisthenics', 'Calisthenics'), ('crossfit', 'Crossfit'), ('bodybuilding', 'Bodybuilding')], max_length=255)),
                ('choice_type', models.CharField(choices=[('fitness_goal', 'Fitness Goal'), ('trainer_specialization', 'Trainer Specialization')], max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='roleapplication',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='roleapplication',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='roleapplication',
            name='fitness_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fitness_applications', to='users.commonchoice'),
        ),
    ]
