from django.contrib import admin
from .models import SportsCenter,Facility,SportsCenterFacility


class SportsCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name', 'location')

class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'sports_center')
    list_filter = ('sports_center',)
    search_fields = ('name', 'sports_center__name')

class SportsCenterFacilityAdmin(admin.ModelAdmin):
    list_display = ('facility', 'available')
    list_filter = ('facility__sports_center',)
    search_fields = ('facility__name', 'facility__sports_center__name')

# Register your models here.
admin.site.register(SportsCenter, SportsCenterAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(SportsCenterFacility, SportsCenterFacilityAdmin)