from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from decimal import Decimal

from .forms import RegisterForm, LoginForm, ProfileForm, TopUpForm
from rentals.models import Rental


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать в DjanCar, {user.first_name}!')
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'С возвращением, {user.first_name or user.username}!')
            return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('core:home')


@login_required
def profile_view(request):
    rentals = Rental.objects.filter(user=request.user).select_related('car').order_by('-created_at')[:10]
    stats = {
        'total_rentals': Rental.objects.filter(user=request.user, status='completed').count(),
        'active_rentals': Rental.objects.filter(user=request.user, status__in=['active', 'reserved']).count(),
    }
    return render(request, 'accounts/profile.html', {
        'rentals': rentals,
        'stats': stats,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def topup_view(request):
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.balance = request.user.balance + Decimal(str(amount))
            request.user.save()
            messages.success(request, f'Баланс пополнен на {amount} ₽')
            return redirect('accounts:profile')
    else:
        form = TopUpForm()
    return render(request, 'accounts/topup.html', {'form': form})
