from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='list'),
    path('api/', views.cars_api, name='api'),
    path('<int:pk>/', views.car_detail, name='detail'),
    path('<int:pk>/review/', views.review_add, name='review_add'),
]
