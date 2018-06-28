from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='sales_index'),
    path('customer/', views.customer_list, name='customer_list')
]
