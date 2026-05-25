from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя для каршеринга."""

    phone = models.CharField('Телефон', max_length=20, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    city = models.CharField('Город', max_length=80, default='Ульяновск')

    driver_license_number = models.CharField('Номер ВУ', max_length=20, blank=True)
    driver_license_issued = models.DateField('Дата выдачи ВУ', null=True, blank=True)
    driver_license_verified = models.BooleanField('Водительские права подтверждены', default=False)

    passport_verified = models.BooleanField('Паспорт подтверждён', default=False)
    is_blocked = models.BooleanField('Заблокирован', default=False)
    balance = models.DecimalField('Баланс, ₽', max_digits=10, decimal_places=2, default=0)
    bonus_points = models.PositiveIntegerField('Бонусные баллы', default=0)
    rating = models.DecimalField('Рейтинг водителя', max_digits=3, decimal_places=2, default=5.00)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        full = self.get_full_name()
        return full if full else self.username

    @property
    def is_verified(self):
        return self.driver_license_verified and self.passport_verified
