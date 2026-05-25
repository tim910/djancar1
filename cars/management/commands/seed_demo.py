"""
Демо-данные для DjanCar.

Запуск: python manage.py seed_demo
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from cars.models import Car, Tariff, CarReview, STATIC_CAR_IMAGES
from rentals.models import PromoCode
from core.models import SiteReview

User = get_user_model()


# Координаты Ульяновска: реальные точки города
ULYANOVSK_ZONES = [
    # name, address, lat, lng, capacity, charger
    ('Соборная площадь',     'пл. Ленина, 1',                54.317825, 48.402539, 15, True),
    ('ТЦ "Аквамолл"',        'Московское шоссе, 108',        54.288812, 48.394567, 25, True),
    ('УлГУ корп. №1',        'ул. Льва Толстого, 42',        54.320145, 48.396712, 12, False),
    ('Парк "Винновская роща"','ул. Александра Невского, 1а', 54.286430, 48.456720, 8,  False),
    ('Аэропорт Баратаевка',  'пр. Авиастроителей, 1',        54.268340, 48.226740, 30, True),
    ('Ж/д вокзал Ульяновск-Центральный', 'пл. Привокзальная, 1', 54.317260, 48.376290, 18, False),
    ('ТРЦ "ЗвезДа"',         'Московское шоссе, 91',         54.291720, 48.408120, 20, True),
    ('Новый Город (центр)',  'пр. Ленинского Комсомола, 39', 54.357480, 48.546790, 22, True),
    ('Засвияжье — Камышинская','ул. Камышинская, 16',        54.291890, 48.328760, 14, False),
    ('Заволжский район — Авиастроителей', 'пр. Авиастроителей, 26', 54.347820, 48.567430, 16, True),
    ('Парк Победы',          'пл. 30-летия Победы',          54.327650, 48.398910, 10, False),
    ('Стадион "Старт"',      'ул. Минаева, 50',              54.319870, 48.387640, 12, False),
]

# Реальные модели автомобилей с фотографиями (Unsplash CDN)
CARS_DATA = [
    # brand, model, year, color, plate, klass, fuel, trans, seats, eng, hp, image_url
    ('Kia', 'Rio', 2023, 'Белый', 'А001АА73', 'economy', 'petrol', 'auto', 5, 1.6, 123,
     'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&q=80'),
    ('Hyundai', 'Solaris', 2023, 'Серебристый', 'А002АА73', 'economy', 'petrol', 'auto', 5, 1.6, 123,
     'https://images.unsplash.com/photo-1502877338535-766e1452684a?w=800&q=80'),
    ('LADA', 'Vesta', 2024, 'Чёрный', 'А003АА73', 'economy', 'petrol', 'manual', 5, 1.6, 106,
     'https://images.unsplash.com/photo-1612825173281-9a193378527e?w=800&q=80'),
    ('LADA', 'Granta', 2023, 'Синий', 'А004АА73', 'economy', 'petrol', 'manual', 5, 1.6, 90,
     'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&q=80'),
    ('Renault', 'Logan', 2022, 'Бежевый', 'А005АА73', 'economy', 'petrol', 'auto', 5, 1.6, 102,
     'https://images.unsplash.com/photo-1568844293986-8d0400bd4745?w=800&q=80'),
    ('Datsun', 'on-DO', 2022, 'Серый', 'А006АА73', 'economy', 'petrol', 'manual', 5, 1.6, 87,
     'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&q=80'),
    ('Volkswagen', 'Polo', 2023, 'Красный', 'А101АА73', 'comfort', 'petrol', 'auto', 5, 1.6, 110,
     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80'),
    ('Skoda', 'Octavia', 2024, 'Серый', 'А102АА73', 'comfort', 'petrol', 'auto', 5, 1.8, 180,
     'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80'),
    ('Toyota', 'Camry', 2024, 'Чёрный', 'А103АА73', 'comfort', 'petrol', 'auto', 5, 2.5, 200,
     'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&q=80'),
    ('Kia', 'K5', 2023, 'Серебристый', 'А104АА73', 'comfort', 'petrol', 'auto', 5, 2.0, 150,
     'https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=800&q=80'),
    ('Mazda', '6', 2023, 'Красный', 'А105АА73', 'comfort', 'petrol', 'auto', 5, 2.5, 192,
     'https://images.unsplash.com/photo-1547744822-0aa1ed2cd9a5?w=800&q=80'),
    ('Kia', 'Optima', 2023, 'Белый', 'А106АА73', 'comfort', 'petrol', 'auto', 5, 2.0, 150,
     'https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=800&q=80'),
    ('Hyundai', 'Creta', 2024, 'Белый', 'А201АА73', 'suv', 'petrol', 'auto', 5, 1.6, 123,
     'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80'),
    ('Kia', 'Sportage', 2024, 'Серый', 'А202АА73', 'suv', 'petrol', 'auto', 5, 2.0, 150,
     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80'),
    ('Renault', 'Duster', 2023, 'Оранжевый', 'А203АА73', 'suv', 'diesel', 'manual', 5, 1.5, 109,
     'https://images.unsplash.com/photo-1568844293986-8d0400bd4745?w=800&q=80'),
    ('Nissan', 'X-Trail', 2024, 'Чёрный', 'А204АА73', 'suv', 'petrol', 'variator', 5, 2.5, 171,
     'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&q=80'),
    ('Geely', 'Coolray', 2024, 'Синий', 'А205АА73', 'suv', 'petrol', 'robot', 5, 1.5, 150,
     'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80'),
    ('BMW', '3 Series', 2024, 'Чёрный', 'А301АА73', 'business', 'petrol', 'auto', 5, 2.0, 245,
     'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80'),
    ('Mercedes-Benz', 'E-Class', 2024, 'Серебристый', 'А302АА73', 'business', 'petrol', 'auto', 5, 2.0, 197,
     'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80'),
    ('Audi', 'A6', 2023, 'Белый', 'А303АА73', 'business', 'petrol', 'auto', 5, 2.0, 245,
     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80'),
    ('Tesla', 'Model 3', 2024, 'Белый', 'А401АА73', 'electro', 'electric', 'auto', 5, 0.0, 283,
     'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80'),
    ('Evolute', 'i-Pro', 2024, 'Синий', 'А402АА73', 'electro', 'electric', 'auto', 5, 0.0, 150,
     'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800&q=80'),
    ('Москвич', '3е', 2024, 'Красный', 'А403АА73', 'electro', 'electric', 'auto', 5, 0.0, 190,
     'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&q=80'),
    ('Porsche', 'Cayenne', 2023, 'Чёрный', 'А501АА73', 'premium', 'petrol', 'auto', 5, 3.0, 340,
     'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800&q=80'),
    ('Mercedes-Benz', 'G-Class', 2024, 'Чёрный', 'А502АА73', 'premium', 'petrol', 'auto', 5, 4.0, 422,
     'https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=800&q=80'),
    ('BMW', 'X7', 2024, 'Белый', 'А503АА73', 'premium', 'petrol', 'auto', 7, 3.0, 340,
     'https://images.unsplash.com/photo-1607853554439-0069ec0f29b6?w=800&q=80'),

    # === ЭКОНОМ — дополнительно ===
    ('LADA', 'Largus', 2023, 'Белый', 'А007АА73', 'economy', 'petrol', 'manual', 7, 1.6, 106,
     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80'),
    ('Chery', 'Tiggo 4', 2024, 'Серый', 'А008АА73', 'economy', 'petrol', 'auto', 5, 1.5, 113,
     'https://images.unsplash.com/photo-1568844293986-8d0400bd4745?w=800&q=80'),
    ('Haval', 'Jolion', 2023, 'Синий', 'А009АА73', 'economy', 'petrol', 'auto', 5, 1.5, 143,
     'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&q=80'),

    # === КОМФОРТ — дополнительно ===
    ('Hyundai', 'Sonata', 2024, 'Чёрный', 'А107АА73', 'comfort', 'petrol', 'auto', 5, 2.5, 180,
     'https://images.unsplash.com/photo-1502877338535-766e1452684a?w=800&q=80'),
    ('Volkswagen', 'Passat', 2023, 'Серебристый', 'А108АА73', 'comfort', 'petrol', 'auto', 5, 1.8, 180,
     'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80'),
    ('Honda', 'Accord', 2023, 'Синий', 'А109АА73', 'comfort', 'petrol', 'auto', 5, 2.0, 192,
     'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80'),

    # === КРОССОВЕР — дополнительно ===
    ('Toyota', 'RAV4', 2024, 'Белый', 'А206АА73', 'suv', 'petrol', 'auto', 5, 2.5, 199,
     'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80'),
    ('Mazda', 'CX-5', 2024, 'Красный', 'А207АА73', 'suv', 'petrol', 'auto', 5, 2.5, 194,
     'https://images.unsplash.com/photo-1547744822-0aa1ed2cd9a5?w=800&q=80'),
    ('Lada', 'Niva Travel', 2023, 'Зелёный', 'А208АА73', 'suv', 'petrol', 'manual', 5, 1.7, 80,
     'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&q=80'),

    # === БИЗНЕС — дополнительно ===
    ('Lexus', 'ES', 2024, 'Чёрный', 'А304АА73', 'business', 'petrol', 'auto', 5, 2.5, 200,
     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80'),
    ('Genesis', 'G80', 2024, 'Серебристый', 'А305АА73', 'business', 'petrol', 'auto', 5, 2.5, 304,
     'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80'),

    # === ЭЛЕКТРО — дополнительно ===
    ('BYD', 'Han', 2024, 'Синий', 'А404АА73', 'electro', 'electric', 'auto', 5, 0.0, 245,
     'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80'),
    ('Voyah', 'Free', 2024, 'Белый', 'А405АА73', 'electro', 'electric', 'auto', 5, 0.0, 503,
     'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800&q=80'),
    ('Zeekr', '001', 2024, 'Серый', 'А406АА73', 'electro', 'electric', 'auto', 5, 0.0, 400,
     'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&q=80'),

    # === ПРЕМИУМ — дополнительно ===
    ('Bentley', 'Continental', 2023, 'Чёрный', 'А504АА73', 'premium', 'petrol', 'auto', 4, 6.0, 626,
     'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800&q=80'),
    ('Range Rover', 'Sport', 2024, 'Чёрный', 'А505АА73', 'premium', 'diesel', 'auto', 5, 3.0, 350,
     'https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=800&q=80'),

    # === КАБРИОЛЕТЫ ===
    ('BMW', 'Z4', 2024, 'Красный', 'А601АА73', 'cabrio', 'petrol', 'auto', 2, 3.0, 340,
     'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80'),
    ('Mazda', 'MX-5', 2023, 'Жёлтый', 'А602АА73', 'cabrio', 'petrol', 'manual', 2, 2.0, 184,
     'https://images.unsplash.com/photo-1547744822-0aa1ed2cd9a5?w=800&q=80'),
    ('Mercedes-Benz', 'SLK', 2023, 'Серебристый', 'А603АА73', 'cabrio', 'petrol', 'auto', 2, 2.0, 245,
     'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80'),

    # === МИНИВЭНЫ ===
    ('Toyota', 'Alphard', 2024, 'Чёрный', 'А701АА73', 'van', 'petrol', 'auto', 7, 2.5, 182,
     'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80'),
    ('Mercedes-Benz', 'V-Class', 2024, 'Серебристый', 'А702АА73', 'van', 'diesel', 'auto', 8, 2.0, 190,
     'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80'),
    ('Volkswagen', 'Multivan', 2023, 'Синий', 'А703АА73', 'van', 'diesel', 'auto', 7, 2.0, 150,
     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80'),

    # === ГРУЗОВЫЕ (ГАЗель) ===
    ('ГАЗ', 'ГАЗель Next', 2023, 'Белый', 'А801АА73', 'truck', 'diesel', 'manual', 3, 2.8, 149,
     'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800&q=80'),
    ('ГАЗ', 'ГАЗель Бизнес', 2022, 'Белый', 'А802АА73', 'truck', 'petrol', 'manual', 3, 2.7, 107,
     'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800&q=80'),
    ('ГАЗ', 'Соболь Бизнес', 2023, 'Серый', 'А803АА73', 'truck', 'petrol', 'manual', 7, 2.7, 107,
     'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&q=80'),
]


class Command(BaseCommand):
    help = 'Загружает демо-данные для DjanCar'

    def handle(self, *args, **opts):
        self.stdout.write(self.style.NOTICE('🌱 Загружаем демо-данные DjanCar...'))

        # 1. Тарифы
        tariff_eco, _ = Tariff.objects.get_or_create(
            name='Эконом', defaults={
                'description': 'Базовый тариф для повседневных поездок',
                'price_per_minute': Decimal('7.00'),
                'price_per_hour': Decimal('290.00'),
                'price_per_day': Decimal('1990.00'),
                'free_kilometers': 200,
            })
        tariff_comfort, _ = Tariff.objects.get_or_create(
            name='Комфорт', defaults={
                'description': 'Просторные авто среднего класса',
                'price_per_minute': Decimal('12.00'),
                'price_per_hour': Decimal('490.00'),
                'price_per_day': Decimal('3490.00'),
                'free_kilometers': 250,
            })
        tariff_business, _ = Tariff.objects.get_or_create(
            name='Бизнес', defaults={
                'description': 'Премиальные авто для деловых поездок',
                'price_per_minute': Decimal('22.00'),
                'price_per_hour': Decimal('890.00'),
                'price_per_day': Decimal('6990.00'),
                'free_kilometers': 300,
            })
        tariff_electro, _ = Tariff.objects.get_or_create(
            name='Электро', defaults={
                'description': 'Экологичные электрокары с зарядкой включённой',
                'price_per_minute': Decimal('9.00'),
                'price_per_hour': Decimal('390.00'),
                'price_per_day': Decimal('2490.00'),
                'free_kilometers': 250,
            })
        tariff_cabrio, _ = Tariff.objects.get_or_create(
            name='Кабриолет', defaults={
                'description': 'Для романтических поездок и фотосессий',
                'price_per_minute': Decimal('28.00'),
                'price_per_hour': Decimal('1190.00'),
                'price_per_day': Decimal('8990.00'),
                'free_kilometers': 200,
            })
        tariff_van, _ = Tariff.objects.get_or_create(
            name='Минивэн', defaults={
                'description': 'Для большой компании или семьи (7-8 мест)',
                'price_per_minute': Decimal('18.00'),
                'price_per_hour': Decimal('690.00'),
                'price_per_day': Decimal('4990.00'),
                'free_kilometers': 300,
            })
        tariff_truck, _ = Tariff.objects.get_or_create(
            name='Грузовой', defaults={
                'description': 'ГАЗели для переездов и перевозок',
                'price_per_minute': Decimal('15.00'),
                'price_per_hour': Decimal('590.00'),
                'price_per_day': Decimal('3990.00'),
                'free_kilometers': 250,
            })
        self.stdout.write(self.style.SUCCESS('  ✓ Тарифы созданы'))

        tariff_map = {
            'economy': tariff_eco,
            'comfort': tariff_comfort,
            'business': tariff_business,
            'suv': tariff_comfort,
            'electro': tariff_electro,
            'premium': tariff_business,
            'cabrio': tariff_cabrio,
            'van': tariff_van,
            'truck': tariff_truck,
        }

        # 2. Автомобили — разбрасываем по Ульяновску в случайных точках
        # Центральные точки города (без сущности ParkingZone)
        spawn_points = [(lat, lng) for _, _, lat, lng, _, _ in ULYANOVSK_ZONES]
        cars_created = 0
        for data in CARS_DATA:
            brand, model, year, color, plate, klass, fuel, trans, seats, eng, hp, _ = data
            if Car.objects.filter(number_plate=plate).exists():
                continue
            base_lat, base_lng = random.choice(spawn_points)
            lat = base_lat + random.uniform(-0.008, 0.008)
            lng = base_lng + random.uniform(-0.008, 0.008)

            # Достаём имя файла из словаря STATIC_CAR_IMAGES автоматически
            full_name = f'{brand} {model}'
            static_path = STATIC_CAR_IMAGES.get(full_name, '')
            # static_path формата 'images/Rio.webp' → выдираем только 'Rio.webp'
            img_filename = static_path.split('/', 1)[1] if '/' in static_path else ''

            Car.objects.create(
                brand=brand, model=model, year=year, color=color,
                number_plate=plate, car_class=klass, fuel_type=fuel,
                transmission=trans, seats=seats,
                engine_volume=Decimal(str(eng)), power_hp=hp,
                fuel_level=random.randint(35, 100),
                mileage=random.randint(5000, 80000),
                has_child_seat=random.random() > 0.7,
                has_winter_tires=True,
                status=random.choices(
                    ['available', 'available', 'available', 'reserved', 'rented', 'service'],
                    weights=[5, 5, 5, 1, 1, 1]
                )[0],
                tariff=tariff_map[klass],
                latitude=Decimal(str(round(lat, 6))),
                longitude=Decimal(str(round(lng, 6))),
                image_filename=img_filename,
                description=f'{brand} {model} {year} года — {color.lower()}. Современный автомобиль в идеальном состоянии.',
                rating=Decimal(str(round(random.uniform(4.3, 5.0), 2))),
                rentals_count=random.randint(20, 350),
            )
            cars_created += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {cars_created} автомобилей'))

        # 4. Промокоды
        future = timezone.now() + timedelta(days=180)
        PromoCode.objects.get_or_create(
            code='WELCOME30',
            defaults={'description': 'Скидка 30% новым клиентам',
                      'discount_percent': 30, 'valid_to': future, 'max_uses': 1000})
        PromoCode.objects.get_or_create(
            code='STUDENT15',
            defaults={'description': 'Скидка 15% для студентов УлГУ',
                      'discount_percent': 15, 'valid_to': future, 'max_uses': 500})
        self.stdout.write(self.style.SUCCESS('  ✓ Промокоды'))

        # 5. Тестовые пользователи
        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user(
                username='demo', password='demo12345',
                email='demo@djancar.ru',
                first_name='Артём', last_name='Иванов',
                phone='+79991234567',
                city='Ульяновск',
                balance=Decimal('2500.00'),
                bonus_points=420,
                driver_license_verified=True,
                passport_verified=True,
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ Демо-пользователь: demo / demo12345'))

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', password='admin12345',
                email='admin@djancar.ru',
                first_name='Админ', last_name='Главный',
            )
            self.stdout.write(self.style.SUCCESS('  ✓ Суперпользователь: admin / admin12345'))

        # 6. Несколько демо-пользователей с разными отзывами на главной
        seed_users = [
            ('alex_m',   'Алексей',  'Морозов',    '★★★★★', 'Каждое утро катаюсь до УлГУ. Дешевле такси и быстрее маршрутки. Авто всегда чистые, реально рекомендую!'),
            ('maria_t',  'Мария',    'Тимофеева',  '★★★★★', 'Брала Hyundai Creta на выходные в Самару. Удобно, что нет ограничения по пробегу. Поддержка реально 24/7 — звонила ночью, ответили.'),
            ('denis_k',  'Денис',    'Кравцов',    '★★★★★', 'Попробовал электрокар Evolute — тише, мягче, дешевле. Теперь только электрички в DjanCar.'),
            ('olga_p',   'Ольга',    'Петрова',    '★★★★★', 'Удобный сайт, регистрация заняла 5 минут. Документы проверили быстро. Тариф «Эконом» для города идеален.'),
            ('ivan_s',   'Иван',     'Соколов',    '★★★★☆', 'Хороший каршеринг, авто заправлены, чистые. Иногда зимой бывает не сразу видно ближайшую машину, но в целом норм.'),
            ('elena_b',  'Елена',    'Бирюкова',   '★★★★★', 'Бронирую на работу каждый день — выходит дешевле такси. Приложение пока сырое, но сайт удобный.'),
        ]
        for uname, fname, lname, _, text in seed_users:
            user, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': fname, 'last_name': lname,
                    'email': f'{uname}@example.com',
                    'city': 'Ульяновск', 'balance': Decimal('500.00'),
                    'driver_license_verified': True, 'passport_verified': True,
                }
            )
            if created:
                user.set_password('demo12345')
                user.save()
            SiteReview.objects.get_or_create(
                user=user,
                defaults={
                    'rating': 5 if '★★★★★' in seed_users[0] else random.randint(4, 5),
                    'text': text,
                }
            )

        # CarReview — отзывы на конкретные авто
        demo_user = User.objects.filter(username='demo').first()
        if demo_user:
            for car in Car.objects.all()[:6]:
                CarReview.objects.get_or_create(
                    car=car, user=demo_user,
                    defaults={
                        'rating': random.randint(4, 5),
                        'text': random.choice([
                            'Отличное авто, чистое, едет мягко. Рекомендую!',
                            'Брал на выходные в Самару — никаких проблем. Удобно.',
                            'Хороший каршеринг, авто всегда заправлены.',
                            'Понравился сайт, всё интуитивно. Авто супер.',
                        ]),
                    }
                )

        self.stdout.write(self.style.SUCCESS('\n✅ Готово! Запусти сервер: python manage.py runserver'))
        self.stdout.write(self.style.WARNING('   Логин для теста — demo / demo12345'))
        self.stdout.write(self.style.WARNING('   Админка     — admin / admin12345'))
