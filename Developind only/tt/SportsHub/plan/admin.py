from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DailyEvents

class DailyEventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'trainer', 'fitness_user')
    search_fields = ('name', 'trainer__username', 'fitness_user__username')  # Add fields you want to search by

admin.site.register(DailyEvents, DailyEventsAdmin)
