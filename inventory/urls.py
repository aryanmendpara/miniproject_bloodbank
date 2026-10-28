from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('movements/', views.stock_movements, name='stock_movements'),
]
