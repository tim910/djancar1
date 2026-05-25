from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse

from cars.models import Car, CarStatus
from .models import Rental, RentalStatus, RentalMode, Payment, PromoCode


@login_required
def reserve_car(request, car_id):
    """Бронирование автомобиля на 20 минут."""
    car = get_object_or_404(Car, pk=car_id)

    if request.user.balance <= settings.MIN_BALANCE_FOR_RENTAL:
        messages.error(
            request,
            f'❌ Недостаточно средств на балансе! '
            f'У вас {request.user.balance} ₽, '
            f'нужно минимум {settings.MIN_BALANCE_FOR_RENTAL} ₽. '
            f'Пополните баланс, чтобы арендовать авто.'
        )
        return redirect('accounts:topup')

    if car.status != CarStatus.AVAILABLE:
        messages.error(request, 'Этот автомобиль сейчас недоступен')
        return redirect('cars:detail', pk=car.pk)

    mode = request.POST.get('mode', RentalMode.MINUTE)
    if mode not in dict(RentalMode.choices):
        mode = RentalMode.MINUTE

    rental = Rental.objects.create(
        user=request.user,
        car=car,
        mode=mode,
        status=RentalStatus.RESERVED,
        start_lat=car.latitude,
        start_lng=car.longitude,
    )
    car.status = CarStatus.RESERVED
    car.save(update_fields=['status'])
    messages.success(request, f'Бронь оформлена на 20 минут. Найдите авто {car.full_name}!')
    return redirect('rentals:detail', pk=rental.pk)


@login_required
def start_rental(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if rental.status != RentalStatus.RESERVED:
        messages.error(request, 'Нельзя стартовать эту аренду')
        return redirect('rentals:detail', pk=pk)
    rental.status = RentalStatus.ACTIVE
    rental.start_time = timezone.now()
    rental.save(update_fields=['status', 'start_time'])
    rental.car.status = CarStatus.RENTED
    rental.car.save(update_fields=['status'])
    messages.success(request, 'Поездка началась! Счастливого пути 🚗')
    return redirect('rentals:detail', pk=pk)


@login_required
def finish_rental(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if rental.status != RentalStatus.ACTIVE:
        messages.error(request, 'Эту аренду нельзя завершить')
        return redirect('rentals:detail', pk=pk)

    rental.end_time = timezone.now()
    rental.total_cost = rental.calculate_cost()

    promo_code = (request.POST.get('promo') or rental.promo_code or '').strip()
    if promo_code:
        try:
            pc = PromoCode.objects.get(code__iexact=promo_code)
            if pc.is_valid():
                discount = (rental.total_cost * Decimal(pc.discount_percent) / Decimal('100')).quantize(Decimal('0.01'))
                rental.discount = discount
                rental.promo_code = pc.code
                pc.uses += 1
                pc.save(update_fields=['uses'])
        except PromoCode.DoesNotExist:
            pass

    rental.final_cost = max(Decimal('0'), rental.total_cost - rental.discount)
    rental.status = RentalStatus.COMPLETED

    user = request.user
    if user.balance >= rental.final_cost:
        user.balance -= rental.final_cost
        user.bonus_points += int(rental.final_cost // 10)
        user.save(update_fields=['balance', 'bonus_points'])
        rental.paid = True
        Payment.objects.create(user=user, rental=rental, kind='rental',
                               amount=rental.final_cost,
                               description=f'Оплата аренды #{rental.id}')
    else:
        messages.warning(request, 'Недостаточно средств — пополните баланс')

    rental.save()
    rental.car.status = CarStatus.AVAILABLE
    rental.car.rentals_count += 1
    rental.car.save(update_fields=['status', 'rentals_count'])

    messages.success(request, f'Поездка завершена. К оплате: {rental.final_cost} ₽')
    return redirect('rentals:detail', pk=rental.pk)


@login_required
def cancel_rental(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if rental.status != RentalStatus.RESERVED:
        messages.error(request, 'Эту аренду уже нельзя отменить')
        return redirect('rentals:detail', pk=pk)
    rental.status = RentalStatus.CANCELLED
    rental.save(update_fields=['status'])
    rental.car.status = CarStatus.AVAILABLE
    rental.car.save(update_fields=['status'])
    messages.info(request, 'Бронь отменена')
    return redirect('rentals:list')


@login_required
def rental_detail(request, pk):
    rental = get_object_or_404(Rental.objects.select_related('car', 'user'),
                                pk=pk, user=request.user)
    return render(request, 'rentals/detail.html', {'rental': rental})


@login_required
def rental_list(request):
    qs = Rental.objects.filter(user=request.user).select_related('car').order_by('-created_at')
    return render(request, 'rentals/list.html', {'rentals': qs})


@login_required
def rate_rental(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 5))
        except ValueError:
            rating = 5
        rental.user_rating = max(1, min(5, rating))
        rental.comment = request.POST.get('comment', '').strip()
        rental.save(update_fields=['user_rating', 'comment'])
        messages.success(request, 'Спасибо за оценку!')
    return redirect('rentals:detail', pk=pk)
