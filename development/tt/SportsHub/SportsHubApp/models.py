from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from users.models import CustomUser
from Members.models import TrainingPlanAssignment


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
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation by {self.reserver} for {self.sport} on {self.reservation_date}"


class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a user
    razorpay_order_id = models.CharField(max_length=255)  # Razorpay order ID
    payment_id = models.CharField(max_length=255)  # Razorpay payment ID
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=3)  # Currency code (e.g., "INR")
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    reservation = models.OneToOneField('Reservation', null=True, blank=True, on_delete=models.SET_NULL)
    TrainingPlanAssignment = models.OneToOneField('Members.TrainingPlanAssignment', null=True, blank=True, on_delete=models.SET_NULL)
 
    def str(self):
        return f"Payment ID: {self.id}, Status: {self.payment_status}"

    class Meta:
        ordering = ['-timestamp']

#Update Status not implemented
    def update_status(self):
        # Calculate the time difference in minutes
        time_difference = (timezone.now() - self.timestamp).total_seconds() / 60

        if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
            # Update the status to "Failed"
            self.payment_status = self.PaymentStatusChoices.FAILED
            self.save()