from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='list'),
    path('api/', views.cars_api, name='api'),
    path('cron/record-positions/', views.cron_record_positions, name='cron_record'),
    path('cron/cleanup-pings/', views.cron_cleanup_pings, name='cron_cleanup'),
    path('<int:pk>/', views.car_detail, name='detail'),
    path('<int:pk>/review/', views.review_add, name='review_add'),
]
