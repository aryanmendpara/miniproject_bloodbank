from django.urls import path
from . import views

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('add/', views.add_donor, name='add_donor'),
    path('<int:pk>/', views.donor_detail, name='donor_detail'),
    path('<int:pk>/edit/', views.edit_donor, name='edit_donor'),
    path('<int:pk>/delete/', views.delete_donor, name='delete_donor'),
]
