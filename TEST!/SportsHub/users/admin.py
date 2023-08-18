from django.contrib import admin
from .models import CustomUser, Role

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
