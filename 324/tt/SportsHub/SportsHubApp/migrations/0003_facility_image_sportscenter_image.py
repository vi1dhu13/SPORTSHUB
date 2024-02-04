# Generated by Django 4.2.4 on 2023-08-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportsHubApp', '0002_alter_facility_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='facilities/'),
        ),
        migrations.AddField(
            model_name='sportscenter',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sports_centers/'),
        ),
    ]
