from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'phone', 'is_verified', 'balance', 'is_blocked')
    list_filter = ('is_blocked', 'driver_license_verified', 'passport_verified', 'is_staff')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Профиль каршеринга', {
            'fields': ('phone', 'avatar', 'birth_date', 'city',
                       'driver_license_number', 'driver_license_issued',
                       'driver_license_verified', 'passport_verified',
                       'is_blocked', 'balance', 'bonus_points', 'rating')
        }),
    )
