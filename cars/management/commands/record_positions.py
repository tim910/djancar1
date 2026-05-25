"""
Записывает GPS-снимок (LocationPing) для каждого активного авто.

Запуск:
    python manage.py record_positions

На Render — настроить Cron Job (или UptimeRobot на endpoint) каждые 5-10 мин.
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone

from cars.models import Car, LocationPing, CarStatus
from rentals.models import Rental, RentalStatus


class Command(BaseCommand):
    help = 'Записывает GPS-снимок позиции для всех активных авто'

    def handle(self, *args, **opts):
        now = timezone.now()
        recorded = 0

        # Снимок для всех авто (свободных и в аренде)
        for car in Car.objects.exclude(status=CarStatus.SERVICE).exclude(status=CarStatus.REPAIR):
            # Привязываем к активной аренде если есть
            active_rental = Rental.objects.filter(
                car=car, status=RentalStatus.ACTIVE
            ).first()

            # Симулируем небольшое смещение для авто в аренде (как будто едет)
            lat = float(car.latitude)
            lng = float(car.longitude)
            speed = 0
            if active_rental:
                # Авто в движении: сдвигаем координаты на ~50-300 метров
                lat += random.uniform(-0.003, 0.003)
                lng += random.uniform(-0.003, 0.003)
                speed = random.randint(20, 80)
                # Обновляем позицию авто в БД
                car.latitude = Decimal(str(round(lat, 6)))
                car.longitude = Decimal(str(round(lng, 6)))
                # Расход топлива/заряда
                if car.fuel_level > 5:
                    car.fuel_level -= 1
                car.save(update_fields=['latitude', 'longitude', 'fuel_level'])

            LocationPing.objects.create(
                car=car,
                rental=active_rental,
                latitude=Decimal(str(round(lat, 6))),
                longitude=Decimal(str(round(lng, 6))),
                speed_kmh=speed,
                fuel_level=car.fuel_level,
            )
            recorded += 1

        self.stdout.write(self.style.SUCCESS(
            f'[{now:%H:%M:%S}] Записано GPS-снимков: {recorded}'
        ))
