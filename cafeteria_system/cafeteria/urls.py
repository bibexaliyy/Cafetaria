from django.urls import path
from .views import home, authenticate_fingerprint, get_meals, select_meal, generate_meal_ticket

urlpatterns = [
    path('', home, name='home'),
    path('authenticate/', authenticate_fingerprint, name='authenticate_fingerprint'),
    path('meals/', get_meals, name='get_meals'),
    path('select-meal/', select_meal, name='select_meal'),
    path('generate_meal_ticket/<int:ticket_id>/', generate_meal_ticket, name='generate_meal_ticket'),
]
