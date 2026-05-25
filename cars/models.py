from django.db import models
from django.urls import reverse
from django.templatetags.static import static


# Маппинг brand+model → файл в static/images/
# Используется когда нет main_image (например на Render free где media/ ephemeral)
STATIC_CAR_IMAGES = {
    'Kia Rio': 'images/Rio.webp',
    'Hyundai Solaris': 'images/solaris.jpg',
    'LADA Vesta': 'images/vesta.webp',
    'LADA Granta': 'images/granta.webp',
    'Renault Logan': 'images/logan.webp',
    'Volkswagen Polo': 'images/polo.webp',
    'Skoda Octavia': 'images/octavia.webp',
    'Toyota Camry': 'images/camry.jpg',
    'Kia K5': 'images/k5.webp',
    'Mazda 6': 'images/mazda 6.webp',
    'Hyundai Creta': 'images/Hyundai Creta.webp',
    'Kia Sportage': 'images/Kia Sportage.jpg',
    'Renault Duster': 'images/Renault Duster.webp',
    'Nissan X-Trail': 'images/Nissan X-Trail.webp',
    'Geely Coolray': 'images/Geely Coolray.webp',
    'Mercedes-Benz E-Class': 'images/e class.jpg',
    'Audi A6': 'images/a6.webp',
    'Tesla Model 3': 'images/Tesla Model 3.jpg',
    'Evolute i-Pro': 'images/e3.webp',
    'Москвич 3е': 'images/3(.webp',
    'Porsche Cayenne': 'images/Porsche Cayenne.webp',
    'Mercedes-Benz G-Class': 'images/Mercedes-Benz G-Class.jpg',
    'BMW X7': 'images/BMW X7.jpg',
    'Kia Optima': 'images/optima.jpg',
    'Datsun on-DO': 'images/датсун он до.webp',
}


def get_static_car_image(full_name):
    """Возвращает URL картинки авто из static по названию марка+модель."""
    filename = STATIC_CAR_IMAGES.get(full_name)
    if filename:
        try:
            return static(filename)
        except Exception:
            pass
    return None


class CarClass(models.TextChoices):
    ECONOMY = 'economy', 'Эконом'
    COMFORT = 'comfort', 'Комфорт'
    BUSINESS = 'business', 'Бизнес'
    SUV = 'suv', 'Кроссовер'
    ELECTRO = 'electro', 'Электрокар'
    PREMIUM = 'premium', 'Премиум'


class FuelType(models.TextChoices):
    PETROL = 'petrol', 'Бензин'
    DIESEL = 'diesel', 'Дизель'
    ELECTRIC = 'electric', 'Электро'
    HYBRID = 'hybrid', 'Гибрид'


class Transmission(models.TextChoices):
    AUTO = 'auto', 'Автомат'
    MANUAL = 'manual', 'Механика'
    ROBOT = 'robot', 'Робот'
    VARIATOR = 'variator', 'Вариатор'


class CarStatus(models.TextChoices):
    AVAILABLE = 'available', 'Свободен'
    RESERVED = 'reserved', 'Забронирован'
    RENTED = 'rented', 'В аренде'
    SERVICE = 'service', 'На обслуживании'
    REPAIR = 'repair', 'В ремонте'


class Tariff(models.Model):
    """Тарифы аренды (поминутный, часовой, суточный)."""

    name = models.CharField('Название тарифа', max_length=80)
    description = models.TextField('Описание', blank=True)
    price_per_minute = models.DecimalField('Цена за минуту, ₽', max_digits=6, decimal_places=2)
    price_per_hour = models.DecimalField('Цена за час, ₽', max_digits=8, decimal_places=2)
    price_per_day = models.DecimalField('Цена за сутки, ₽', max_digits=8, decimal_places=2)
    free_kilometers = models.PositiveIntegerField('Бесплатных км в сутки', default=200)
    extra_km_price = models.DecimalField('Цена за доп. км', max_digits=5, decimal_places=2, default=10)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ('price_per_minute',)

    def __str__(self):
        return f'{self.name} ({self.price_per_minute}₽/мин)'


class ParkingZone(models.Model):
    """Парковочная зона DjanCar в Ульяновске."""

    name = models.CharField('Название', max_length=100)
    address = models.CharField('Адрес', max_length=200)
    description = models.TextField('Описание', blank=True)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6)
    capacity = models.PositiveIntegerField('Вместимость', default=10)
    has_charger = models.BooleanField('Зарядка для электрокаров', default=False)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Парковочная зона'
        verbose_name_plural = 'Парковочные зоны'

    def __str__(self):
        return f'{self.name} — {self.address}'


class Car(models.Model):
    """Автомобиль в парке каршеринга."""

    brand = models.CharField('Марка', max_length=50)
    model = models.CharField('Модель', max_length=50)
    year = models.PositiveIntegerField('Год выпуска')
    color = models.CharField('Цвет', max_length=30)
    number_plate = models.CharField('Гос. номер', max_length=15, unique=True)
    vin = models.CharField('VIN', max_length=17, blank=True)

    car_class = models.CharField('Класс', max_length=20, choices=CarClass.choices, default=CarClass.ECONOMY)
    fuel_type = models.CharField('Топливо', max_length=20, choices=FuelType.choices, default=FuelType.PETROL)
    transmission = models.CharField('Коробка', max_length=20, choices=Transmission.choices, default=Transmission.AUTO)
    seats = models.PositiveSmallIntegerField('Мест', default=5)
    engine_volume = models.DecimalField('Объём двигателя, л', max_digits=3, decimal_places=1, default=1.6)
    power_hp = models.PositiveIntegerField('Мощность, л.с.', default=100)

    fuel_level = models.PositiveSmallIntegerField('Уровень топлива/заряда, %', default=100)
    mileage = models.PositiveIntegerField('Пробег, км', default=0)
    has_child_seat = models.BooleanField('Детское кресло', default=False)
    has_winter_tires = models.BooleanField('Зимняя резина', default=True)

    status = models.CharField('Статус', max_length=20, choices=CarStatus.choices, default=CarStatus.AVAILABLE)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, related_name='cars', verbose_name='Тариф')
    current_zone = models.ForeignKey(ParkingZone, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='cars', verbose_name='Парковочная зона')

    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6)

    main_image = models.ImageField('Главное фото (загрузить)', upload_to='cars/', blank=True, null=True)
    image_filename = models.CharField(
        'Имя файла в static/images/',
        max_length=200, blank=True,
        help_text='Например: optima.jpg или Kia Sportage.jpg. '
                  'Используется когда нет загруженного фото. '
                  'Файл сначала залей в папку static/images/ через GitHub.'
    )
    description = models.TextField('Описание', blank=True)
    rating = models.DecimalField('Рейтинг', max_digits=3, decimal_places=2, default=5.00)
    rentals_count = models.PositiveIntegerField('Кол-во аренд', default=0)

    created_at = models.DateTimeField('Добавлен', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ('brand', 'model')

    def __str__(self):
        return f'{self.brand} {self.model} ({self.number_plate})'

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f'{self.brand} {self.model}'

    @property
    def is_electric(self):
        return self.fuel_type == 'electric'

    @property
    def fuel_label(self):
        """«заряда батареи» для электро, «топлива» для остальных."""
        return 'заряда' if self.is_electric else 'топлива'

    @property
    def fuel_icon(self):
        return '🔋' if self.is_electric else '⛽'

    @property
    def photo_url(self):
        """URL картинки: image_filename (поле в админке) → загруженная → fallback dict → заглушка."""
        # 1. Имя файла из админки (главный путь)
        if self.image_filename:
            try:
                return static(f'images/{self.image_filename}')
            except Exception:
                pass
        # 2. Загруженное фото (на Render free не работает — media ephemeral)
        if self.main_image:
            try:
                return self.main_image.url
            except Exception:
                pass
        # 3. Fallback из словаря STATIC_CAR_IMAGES
        static_url = get_static_car_image(self.full_name)
        if static_url:
            return static_url
        # 4. Заглушка
        return 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80'

    @property
    def is_available(self):
        return self.status == CarStatus.AVAILABLE

    @property
    def status_color(self):
        return {
            'available': 'success',
            'reserved': 'warning',
            'rented': 'danger',
            'service': 'info',
            'repair': 'secondary',
        }.get(self.status, 'secondary')


class CarImage(models.Model):
    """Дополнительные фотографии автомобиля."""

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Фото', upload_to='cars/gallery/')
    caption = models.CharField('Подпись', max_length=100, blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото авто'
        verbose_name_plural = 'Фото авто'
        ordering = ('order',)

    def __str__(self):
        return f'Фото {self.car} #{self.order}'


class CarReview(models.Model):
    """Отзыв об автомобиле."""

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)
        unique_together = ('car', 'user')

    def __str__(self):
        return f'Отзыв {self.user} о {self.car}'
