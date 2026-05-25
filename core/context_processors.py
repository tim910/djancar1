from django.conf import settings


def global_settings(request):
    user = getattr(request, 'user', None)
    low_balance = False
    if user is not None and user.is_authenticated:
        try:
            low_balance = user.balance <= settings.MIN_BALANCE_FOR_RENTAL
        except Exception:
            low_balance = False

    return {
        'YANDEX_MAPS_API_KEY': settings.YANDEX_MAPS_API_KEY,
        'MIN_BALANCE': settings.MIN_BALANCE_FOR_RENTAL,
        'LOW_BALANCE': low_balance,
        'SITE_NAME': 'DjanCar',
        'SITE_CITY': 'Ульяновск',
        'SITE_TAGLINE': 'Современный каршеринг Ульяновска',
    }
