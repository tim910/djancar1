from django.contrib import admin
from .models import FeedbackMessage, SiteReview


@admin.register(SiteReview)
class SiteReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'short_text', 'is_published', 'created_at')
    list_filter = ('rating', 'is_published')
    search_fields = ('user__username', 'user__first_name', 'text')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'

    def short_text(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    short_text.short_description = 'Текст'


@admin.register(FeedbackMessage)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'is_processed', 'created_at')
    list_filter = ('is_processed',)
    search_fields = ('name', 'email', 'subject')
