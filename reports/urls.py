from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('export/donors/', views.export_donors_csv, name='export_donors'),
    path('export/donations/', views.export_donations_csv, name='export_donations'),
    path('export/inventory/', views.export_inventory_csv, name='export_inventory'),
    path('export/requests/', views.export_requests_csv, name='export_requests'),
]
