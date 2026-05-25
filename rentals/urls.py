from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.rental_list, name='list'),
    path('<int:pk>/', views.rental_detail, name='detail'),
    path('reserve/<int:car_id>/', views.reserve_car, name='reserve'),
    path('<int:pk>/start/', views.start_rental, name='start'),
    path('<int:pk>/finish/', views.finish_rental, name='finish'),
    path('<int:pk>/cancel/', views.cancel_rental, name='cancel'),
    path('<int:pk>/rate/', views.rate_rental, name='rate'),
]
