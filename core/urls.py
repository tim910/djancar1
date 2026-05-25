from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map_view, name='map'),
    path('about/', views.about, name='about'),
    path('tariffs/', views.tariffs_page, name='tariffs'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
]
