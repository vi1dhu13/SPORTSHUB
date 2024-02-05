from django.contrib import admin
from .models import CustomUser, Role

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)

from django.contrib import admin
from .models import CommonChoice

class CommonChoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'choice_type']

admin.site.register(CommonChoice, CommonChoiceAdmin)

# YourApp/admin.py

from django.contrib import admin
from .models import RoleApplication

@admin.register(RoleApplication)
class RoleApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_approved']
    list_filter = ['is_approved', 'role']
    search_fields = ['user__username', 'role__name', 'specialization_details', 'fitness_goal__name']

