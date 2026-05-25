from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarImage, CarReview, Tariff, ParkingZone


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'full_name', 'number_plate', 'car_class',
                    'status_badge', 'fuel_level', 'tariff', 'current_zone')
    list_filter = ('status', 'car_class', 'fuel_type', 'transmission', 'tariff')
    search_fields = ('brand', 'model', 'number_plate', 'vin')
    inlines = [CarImageInline]
    list_editable = ('fuel_level',)
    readonly_fields = ('rating', 'rentals_count', 'created_at', 'updated_at')

    fieldsets = (
        ('Основное', {'fields': ('brand', 'model', 'year', 'color',
                                   'number_plate', 'vin', 'main_image', 'description')}),
        ('Характеристики', {'fields': ('car_class', 'fuel_type', 'transmission',
                                         'seats', 'engine_volume', 'power_hp',
                                         'has_child_seat', 'has_winter_tires')}),
        ('Состояние', {'fields': ('status', 'fuel_level', 'mileage',
                                    'tariff', 'current_zone',
                                    'latitude', 'longitude')}),
        ('Статистика', {'fields': ('rating', 'rentals_count', 'created_at', 'updated_at')}),
    )

    def thumb(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:48px;border-radius:6px"/>', obj.main_image.url)
        return '—'
    thumb.short_description = 'Фото'

    def status_badge(self, obj):
        colors = {'available': '#10b981', 'reserved': '#f59e0b', 'rented': '#ef4444',
                  'service': '#3b82f6', 'repair': '#6b7280'}
        return format_html('<span style="padding:3px 10px;border-radius:12px;color:#fff;'
                           'background:{};font-size:12px">{}</span>',
                           colors.get(obj.status, '#6b7280'), obj.get_status_display())
    status_badge.short_description = 'Статус'


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_minute', 'price_per_hour', 'price_per_day', 'is_active')
    list_filter = ('is_active',)


@admin.register(ParkingZone)
class ParkingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity', 'has_charger', 'is_active')
    list_filter = ('is_active', 'has_charger')
    search_fields = ('name', 'address')


@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('car__brand', 'car__model', 'user__username')
