from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

# Create your models here.

class SportsCenter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    description = HTMLField(default=True, blank=True)

    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField(default=True, blank=True)
    sports_center = models.OneToOneField(SportsCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SportsCenterFacility(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.facility.name} - {self.facility.sports_center.name}"
