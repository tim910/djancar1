"""
Дампит все актуальные GPS-снимки в JSON-файл — на случай падения БД.

Запуск:
    python manage.py dump_pings_json
    python manage.py dump_pings_json --path /tmp/pings.json
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

from cars.models import LocationPing


class Command(BaseCommand):
    help = 'Сохраняет GPS-снимки в JSON-файл'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default='',
                            help='Куда сохранить (по умолчанию BASE_DIR/backup/pings.json)')

    def handle(self, *args, **opts):
        path = opts['path']
        if not path:
            backup_dir = Path(settings.BASE_DIR) / 'backup'
            backup_dir.mkdir(exist_ok=True)
            path = backup_dir / 'pings.json'

        data = [{
            'car_id': p.car_id,
            'car': str(p.car),
            'rental_id': p.rental_id,
            'lat': float(p.latitude),
            'lng': float(p.longitude),
            'speed': p.speed_kmh,
            'fuel': p.fuel_level,
            'at': p.recorded_at.isoformat(),
        } for p in LocationPing.objects.select_related('car').all()[:10000]]

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f'Сохранено {len(data)} GPS-снимков в {path}'
        ))
