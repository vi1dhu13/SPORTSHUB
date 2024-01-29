# Generated by Django 4.2.5 on 2023-09-28 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SportsHubApp', '0004_remove_sportscenterfacility_facility_delete_facility_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportsCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField(blank=True, default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='sports_centers/')),
            ],
        ),
        migrations.CreateModel(
            name='SportscenterSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateField()),
                ('reservation_time', models.DateTimeField(auto_now_add=True)),
                ('reserver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='SportsHubApp.sportscenterslot')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SportsHubApp.sportscenter')),
            ],
        ),
    ]
