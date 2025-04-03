from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 'profile_picture')}),
        ('Doctor Info', {'fields': ('specialization', 'license_number', 'years_of_experience')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 'profile_picture')}),
        ('Doctor Info', {'fields': ('specialization', 'license_number', 'years_of_experience')}),
    )

admin.site.register(CustomUser, CustomUserAdmin) 