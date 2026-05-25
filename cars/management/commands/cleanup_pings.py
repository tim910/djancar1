"""
Удаляет GPS-снимки старше 7 дней (по умолчанию).
Запускать раз в день через cron.

Запуск:
    python manage.py cleanup_pings
    python manage.py cleanup_pings --days 14  # хранить 14 дней
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from cars.models import LocationPing


class Command(BaseCommand):
    help = 'Удаляет старые GPS-снимки чтобы БД не разрасталась'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=7,
                            help='Хранить N последних дней (по умолчанию 7)')

    def handle(self, *args, **opts):
        days = opts['days']
        threshold = timezone.now() - timedelta(days=days)
        deleted, _ = LocationPing.objects.filter(recorded_at__lt=threshold).delete()
        self.stdout.write(self.style.SUCCESS(
            f'Удалено GPS-снимков старше {days} дней: {deleted}'
        ))
