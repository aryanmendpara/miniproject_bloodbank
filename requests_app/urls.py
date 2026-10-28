from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('add/', views.add_request, name='add_request'),
    path('<int:pk>/process/', views.process_request, name='process_request'),
]
