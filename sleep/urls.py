from django.urls import path
from . import views

urlpatterns = [
    path('', views.sleep_list, name='sleep_list'),
    path('add/', views.sleep_add, name='sleep_add'),
    path('edit/<int:pk>/', views.sleep_edit, name='sleep_edit'),
    path('delete/<int:pk>/', views.sleep_delete, name='sleep_delete'),
    path('chart/', views.sleep_chart, name='sleep_chart'),
]
