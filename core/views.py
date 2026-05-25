from django.shortcuts import render
from django.db.models import Count, Avg
from cars.models import Car, CarStatus, ParkingZone, Tariff, CarClass


def home(request):
    """Главная страница."""
    available_cars = Car.objects.filter(status=CarStatus.AVAILABLE).select_related('tariff')
    featured_cars = available_cars.order_by('-rating')[:6]

    stats = {
        'cars_total': Car.objects.count(),
        'cars_available': available_cars.count(),
        'zones_total': ParkingZone.objects.filter(is_active=True).count(),
        'happy_clients': 5800,
    }

    tariffs = Tariff.objects.filter(is_active=True)
    classes_summary = (Car.objects.values('car_class')
                       .annotate(cnt=Count('id'), avg_price=Avg('tariff__price_per_minute'))
                       .order_by('car_class'))

    return render(request, 'core/home.html', {
        'featured_cars': featured_cars,
        'stats': stats,
        'tariffs': tariffs,
        'classes_summary': classes_summary,
    })


def map_view(request):
    """Страница интерактивной карты."""
    zones = ParkingZone.objects.filter(is_active=True)
    zones_data = [{
        'name': z.name,
        'address': z.address,
        'lat': float(z.latitude),
        'lng': float(z.longitude),
        'charger': z.has_charger,
    } for z in zones]
    return render(request, 'core/map.html', {
        'zones': zones,
        'zones_data': zones_data,
    })


def about(request):
    return render(request, 'core/about.html')


def tariffs_page(request):
    tariffs = Tariff.objects.filter(is_active=True)
    return render(request, 'core/tariffs.html', {'tariffs': tariffs})


def faq(request):
    questions = [
        ('Что нужно, чтобы пользоваться DjanCar?',
         'Возраст 21+, стаж от 2 лет, паспорт РФ и водительское удостоверение. '
         'Загрузите документы в профиле — модератор проверит их за 15 минут.'),
        ('Как оплачивается аренда?',
         'Оплата списывается с баланса автоматически после завершения поездки. '
         'Пополнить баланс можно картой Visa, Mastercard, МИР или через СБП.'),
        ('Что входит в стоимость?',
         'Бензин, страховка КАСКО и ОСАГО, мойка раз в трое суток, ТО и зимняя резина.'),
        ('Где можно завершить поездку?',
         'В любой жёлтой зоне на карте — это разрешённые парковки в Ульяновске и пригороде.'),
        ('Что делать при ДТП?',
         'Включите аварийку, выставьте знак, сфотографируйте всё и сразу позвоните в поддержку 24/7: 8 800 555-12-34.'),
        ('А если закончился бензин?',
         'Если бак ниже 15% — заправьтесь на любой АЗС и получите скидку 200 ₽ на поездку.'),
    ]
    return render(request, 'core/faq.html', {'questions': questions})


def contacts(request):
    return render(request, 'core/contacts.html')
