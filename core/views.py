from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Avg
from cars.models import Car, CarStatus, Tariff, CarClass
from .models import SiteReview


def home(request):
    """Главная страница."""
    # Приём отзыва
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('review_text', '').strip()
        try:
            rating = int(request.POST.get('review_rating', 5))
        except (ValueError, TypeError):
            rating = 5
        rating = max(1, min(5, rating))
        if text:
            SiteReview.objects.create(user=request.user, rating=rating, text=text)
            messages.success(request, 'Спасибо за отзыв! Он опубликован на главной.')
        else:
            messages.error(request, 'Напишите текст отзыва')
        return redirect('core:home')

    available_cars = Car.objects.filter(status=CarStatus.AVAILABLE).select_related('tariff')
    featured_cars = available_cars.order_by('-rating')[:6]

    stats = {
        'cars_total': Car.objects.count(),
        'cars_available': available_cars.count(),
        'happy_clients': 5800,
        'reviews_count': SiteReview.objects.filter(is_published=True).count(),
    }

    tariffs = Tariff.objects.filter(is_active=True)
    classes_summary = (Car.objects.values('car_class')
                       .annotate(cnt=Count('id'), avg_price=Avg('tariff__price_per_minute'))
                       .order_by('car_class'))

    reviews = (SiteReview.objects.filter(is_published=True)
               .select_related('user')[:9])

    return render(request, 'core/home.html', {
        'featured_cars': featured_cars,
        'stats': stats,
        'tariffs': tariffs,
        'classes_summary': classes_summary,
        'reviews': reviews,
    })


def map_view(request):
    """Страница интерактивной карты."""
    return render(request, 'core/map.html', {})


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
