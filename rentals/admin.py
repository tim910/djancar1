from django.contrib import admin
from .models import Rental, Payment, PromoCode


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'mode', 'status',
                    'start_time', 'end_time', 'final_cost', 'paid')
    list_filter = ('status', 'mode', 'paid')
    search_fields = ('user__username', 'car__brand', 'car__model', 'car__number_plate')
    readonly_fields = ('created_at', 'updated_at', 'duration_minutes')
    date_hierarchy = 'created_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'kind', 'amount', 'rental', 'created_at')
    list_filter = ('kind',)
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'uses', 'max_uses',
                    'valid_to', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)
