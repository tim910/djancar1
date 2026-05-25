from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarImage, CarReview, Tariff, LocationPing


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 2
    fields = ('image', 'caption', 'order', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px;border-radius:8px;object-fit:cover"/>',
                obj.image.url
            )
        return '—'
    preview.short_description = 'Предпросмотр'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'full_name', 'number_plate', 'car_class',
                    'status_badge', 'fuel_level', 'tariff')
    list_filter = ('status', 'car_class', 'fuel_type', 'transmission', 'tariff')
    search_fields = ('brand', 'model', 'number_plate', 'vin')
    inlines = [CarImageInline]
    list_editable = ('fuel_level',)
    readonly_fields = ('rating', 'rentals_count', 'created_at', 'updated_at', 'main_image_preview')

    fieldsets = (
        ('📸 Фотография', {
            'fields': ('image_filename', 'main_image', 'main_image_preview'),
            'description': 'РЕКОМЕНДУЕТСЯ: впишите имя файла из static/images/ '
                           '(например "optima.jpg") — это работает и на Render. '
                           'Загрузка через "Главное фото" работает только локально.',
        }),
        ('🚗 Основное', {
            'fields': ('brand', 'model', 'year', 'color',
                       'number_plate', 'vin', 'description'),
        }),
        ('⚙️ Характеристики', {
            'fields': ('car_class', 'fuel_type', 'transmission',
                       'seats', 'engine_volume', 'power_hp',
                       'has_child_seat', 'has_winter_tires'),
        }),
        ('📍 Состояние и местоположение', {
            'fields': ('status', 'fuel_level', 'mileage',
                       'tariff', 'latitude', 'longitude'),
        }),
        ('📊 Статистика', {
            'fields': ('rating', 'rentals_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def main_image_preview(self, obj):
        url = obj.photo_url
        if url:
            source = 'загруженное' if obj.main_image else 'из static/images/'
            return format_html(
                '<div><img src="{}" style="max-width:400px;max-height:280px;border-radius:12px;'
                'box-shadow:0 4px 16px rgba(0,0,0,0.15)"/></div>'
                '<small style="color:#888">источник: {}</small>',
                url, source
            )
        return format_html('<em style="color:#999">Нет фото</em>')
    main_image_preview.short_description = 'Превью главного фото'

    def thumb(self, obj):
        url = obj.photo_url
        if url:
            return format_html(
                '<img src="{}" style="height:56px;width:84px;object-fit:cover;border-radius:6px"/>',
                url
            )
        return format_html('<span style="color:#bbb;font-size:11px">нет фото</span>')
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


@admin.register(LocationPing)
class LocationPingAdmin(admin.ModelAdmin):
    list_display = ('car', 'latitude', 'longitude', 'speed_kmh', 'fuel_level', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('car__brand', 'car__model', 'car__number_plate')
    date_hierarchy = 'recorded_at'
    readonly_fields = ('car', 'rental', 'latitude', 'longitude', 'speed_kmh',
                       'fuel_level', 'recorded_at')


@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'short_text', 'created_at')
    list_filter = ('rating',)
    search_fields = ('car__brand', 'car__model', 'user__username', 'text')

    def short_text(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    short_text.short_description = 'Отзыв'
