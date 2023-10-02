from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from users.models import CustomUser


class SportsCenter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = HTMLField(default=True, blank=True)
    image = models.ImageField(upload_to='sports_centers/', blank=True, null=True)
    price_per_slot = models.DecimalField(
        max_digits=10,  # Adjust the number of digits as needed
        decimal_places=2,  # Specify the number of decimal places
        blank=True,
        null=True
    )
    def __str__(self):
        return self.name

from django.db import models

class SportscenterSlot(models.Model):
 
    start_time = models.TimeField()
    end_time = models.TimeField()

from django.db import models
from .models import SportscenterSlot  # Assuming 'sportscenter' is the app name

class Reservation(models.Model):
    """
    Model to represent sports center slot reservations.
    """
    reserver = models.ForeignKey(
        CustomUser,  # Replace with your user model
        on_delete=models.CASCADE,
        related_name='reservations',  # A related name for reverse lookups
    )

    sport = models.ForeignKey(
        SportsCenter,  # Replace with your Sport model
        on_delete=models.CASCADE,
    )

    slot = models.ForeignKey(
        SportscenterSlot,
        on_delete=models.CASCADE,
        related_name='reservations',  # A related name for reverse lookups
    )

    reservation_date = models.DateField()
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.reserver} for {self.sport} on {self.reservation_date}"