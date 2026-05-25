from decimal import Decimal
from django.db import models
from django.utils import timezone


class RentalStatus(models.TextChoices):
    RESERVED = 'reserved', 'Забронирован'
    ACTIVE = 'active', 'В аренде'
    COMPLETED = 'completed', 'Завершена'
    CANCELLED = 'cancelled', 'Отменена'


class RentalMode(models.TextChoices):
    MINUTE = 'minute', 'Поминутно'
    HOUR = 'hour', 'Почасово'
    DAY = 'day', 'Посуточно'


class Rental(models.Model):
    """Аренда автомобиля."""

    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT,
                             related_name='rentals', verbose_name='Пользователь')
    car = models.ForeignKey('cars.Car', on_delete=models.PROTECT,
                            related_name='rentals', verbose_name='Автомобиль')

    mode = models.CharField('Тарификация', max_length=10,
                            choices=RentalMode.choices, default=RentalMode.MINUTE)
    status = models.CharField('Статус', max_length=15,
                              choices=RentalStatus.choices, default=RentalStatus.RESERVED)

    start_time = models.DateTimeField('Начало аренды', null=True, blank=True)
    end_time = models.DateTimeField('Окончание аренды', null=True, blank=True)
    planned_end = models.DateTimeField('Планируемое окончание', null=True, blank=True)

    start_address = models.CharField('Адрес начала', max_length=200, blank=True)
    end_address = models.CharField('Адрес окончания', max_length=200, blank=True)
    start_lat = models.DecimalField('Стартовая широта', max_digits=9, decimal_places=6, null=True, blank=True)
    start_lng = models.DecimalField('Стартовая долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    end_lat = models.DecimalField('Конечная широта', max_digits=9, decimal_places=6, null=True, blank=True)
    end_lng = models.DecimalField('Конечная долгота', max_digits=9, decimal_places=6, null=True, blank=True)

    distance_km = models.DecimalField('Пробег, км', max_digits=8, decimal_places=2, default=0)
    total_cost = models.DecimalField('Стоимость, ₽', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Скидка, ₽', max_digits=10, decimal_places=2, default=0)
    final_cost = models.DecimalField('Итого к оплате, ₽', max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField('Оплачено', default=False)

    promo_code = models.CharField('Промокод', max_length=30, blank=True)
    user_rating = models.PositiveSmallIntegerField('Оценка поездки', null=True, blank=True)
    comment = models.TextField('Комментарий', blank=True)

    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Аренда #{self.id} — {self.car} ({self.user})'

    @property
    def duration_minutes(self):
        if not self.start_time:
            return 0
        end = self.end_time or timezone.now()
        return int((end - self.start_time).total_seconds() // 60)

    @property
    def status_color(self):
        return {
            'reserved': 'warning',
            'active': 'success',
            'completed': 'primary',
            'cancelled': 'secondary',
        }.get(self.status, 'secondary')

    def calculate_cost(self):
        """Базовый расчёт стоимости по выбранному режиму."""
        if not self.car or not self.car.tariff:
            return Decimal('0')
        t = self.car.tariff
        minutes = Decimal(self.duration_minutes)
        if self.mode == RentalMode.MINUTE:
            cost = minutes * t.price_per_minute
        elif self.mode == RentalMode.HOUR:
            hours = (minutes / Decimal('60')).quantize(Decimal('0.01'))
            cost = hours * t.price_per_hour
        else:
            days = (minutes / Decimal('1440')).quantize(Decimal('0.01'))
            cost = days * t.price_per_day
        return cost.quantize(Decimal('0.01'))


class Payment(models.Model):
    """История платежей (пополнения/списания)."""

    KIND_CHOICES = (
        ('topup', 'Пополнение'),
        ('rental', 'Оплата аренды'),
        ('bonus', 'Бонус'),
        ('fine', 'Штраф'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payments')
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    kind = models.CharField('Тип', max_length=10, choices=KIND_CHOICES)
    amount = models.DecimalField('Сумма, ₽', max_digits=10, decimal_places=2)
    description = models.CharField('Описание', max_length=200, blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ('-created_at',)


class PromoCode(models.Model):
    """Промокоды на скидки."""
    code = models.CharField('Код', max_length=30, unique=True)
    description = models.CharField('Описание', max_length=200, blank=True)
    discount_percent = models.PositiveSmallIntegerField('Скидка, %', default=10)
    max_uses = models.PositiveIntegerField('Максимум использований', default=100)
    uses = models.PositiveIntegerField('Использовано', default=0)
    valid_from = models.DateTimeField('Действует с', default=timezone.now)
    valid_to = models.DateTimeField('Действует до')
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return (self.is_active and self.valid_from <= now <= self.valid_to
                and self.uses < self.max_uses)
