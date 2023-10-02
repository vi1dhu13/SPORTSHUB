from django.contrib import admin
from .models import SportsCenter, SportscenterSlot, Reservation
@admin.register(SportsCenter)
class SportsCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'description')  # Customize the displayed fields
    list_filter = ('location',)  # Add filters for the 'location' field, if needed

@admin.register(SportscenterSlot)
class SportscenterSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')  # Customize the displayed fields
    list_filter = ('start_time', 'end_time')  # Add filters for the time fields, if needed

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reserver', 'sport', 'slot', 'reservation_date', 'reservation_time')  # Customize the displayed fields
    list_filter = ('reservation_date', 'sport', 'slot')  # Add filters for relevant fields, if needed
