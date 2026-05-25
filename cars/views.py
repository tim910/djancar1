from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Car, CarReview, CarClass, FuelType, Transmission


def car_list(request):
    """Каталог автомобилей с фильтрами."""
    qs = Car.objects.select_related('tariff', 'current_zone').all()

    car_class = request.GET.get('class')
    fuel = request.GET.get('fuel')
    transmission = request.GET.get('transmission')
    status = request.GET.get('status')
    search = request.GET.get('q')
    sort = request.GET.get('sort', '-rating')

    if car_class:
        qs = qs.filter(car_class=car_class)
    if fuel:
        qs = qs.filter(fuel_type=fuel)
    if transmission:
        qs = qs.filter(transmission=transmission)
    if status:
        qs = qs.filter(status=status)
    if search:
        qs = qs.filter(Q(brand__icontains=search) |
                       Q(model__icontains=search) |
                       Q(number_plate__icontains=search))

    allowed_sort = ('rating', '-rating', 'tariff__price_per_minute',
                    '-tariff__price_per_minute', 'year', '-year')
    if sort in allowed_sort:
        qs = qs.order_by(sort)

    return render(request, 'cars/list.html', {
        'cars': qs,
        'car_classes': CarClass.choices,
        'fuel_types': FuelType.choices,
        'transmissions': Transmission.choices,
        'filters': {
            'class': car_class or '',
            'fuel': fuel or '',
            'transmission': transmission or '',
            'status': status or '',
            'q': search or '',
            'sort': sort,
        },
    })


def car_detail(request, pk):
    car = get_object_or_404(Car.objects.select_related('tariff', 'current_zone'), pk=pk)
    reviews = car.reviews.select_related('user').all()[:20]
    similar = Car.objects.filter(car_class=car.car_class).exclude(pk=car.pk)[:4]
    return render(request, 'cars/detail.html', {
        'car': car,
        'reviews': reviews,
        'similar': similar,
    })


def cars_api(request):
    """JSON API для отрисовки маркеров на карте."""
    qs = Car.objects.select_related('tariff', 'current_zone').all()

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    data = [{
        'id': c.id,
        'name': c.full_name,
        'plate': c.number_plate,
        'class': c.get_car_class_display(),
        'status': c.status,
        'status_label': c.get_status_display(),
        'fuel_level': c.fuel_level,
        'fuel_type': c.get_fuel_type_display(),
        'transmission': c.get_transmission_display(),
        'price_per_minute': float(c.tariff.price_per_minute),
        'price_per_hour': float(c.tariff.price_per_hour),
        'price_per_day': float(c.tariff.price_per_day),
        'image': c.photo_url,
        'lat': float(c.latitude),
        'lng': float(c.longitude),
        'url': c.get_absolute_url(),
        'rating': float(c.rating),
    } for c in qs]

    return JsonResponse({'cars': data, 'count': len(data)})


@login_required
def review_add(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        try:
            rating = int(request.POST.get('rating', 5))
        except ValueError:
            rating = 5
        rating = max(1, min(5, rating))
        if text:
            CarReview.objects.update_or_create(
                car=car, user=request.user,
                defaults={'text': text, 'rating': rating},
            )
            messages.success(request, 'Спасибо за отзыв!')
    return car_detail(request, pk)
