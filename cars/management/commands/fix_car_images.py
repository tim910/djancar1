"""
Одноразовая команда: заполняет поле image_filename у существующих авто
из словаря STATIC_CAR_IMAGES. Не трогает авто, у которых поле уже заполнено.

Запуск:
    python manage.py fix_car_images           # только пустые
    python manage.py fix_car_images --force   # перезаписать все
"""
from django.core.management.base import BaseCommand
from cars.models import Car, STATIC_CAR_IMAGES


class Command(BaseCommand):
    help = 'Заполняет image_filename у авто из STATIC_CAR_IMAGES'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Перезаписать image_filename даже если уже заполнено'
        )

    def handle(self, *args, **opts):
        force = opts.get('force', False)
        updated = 0
        skipped = 0
        not_found = []

        for car in Car.objects.all():
            static_path = STATIC_CAR_IMAGES.get(car.full_name, '')
            if not static_path:
                not_found.append(car.full_name)
                continue

            filename = static_path.split('/', 1)[1] if '/' in static_path else static_path

            if car.image_filename and not force:
                skipped += 1
                continue

            car.image_filename = filename
            car.save(update_fields=['image_filename'])
            updated += 1
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ {car.full_name} → {filename}'
            ))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Обновлено: {updated}'))
        if skipped:
            self.stdout.write(self.style.WARNING(
                f'⏭️  Пропущено (уже заполнено): {skipped}. Используй --force, чтобы перезаписать.'
            ))
        if not_found:
            self.stdout.write(self.style.WARNING(
                f'❓ Нет в словаре STATIC_CAR_IMAGES: {", ".join(not_found)}'
            ))
