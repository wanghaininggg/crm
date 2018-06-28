from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='admin_index'),
    path('<str:app_name>/<str:tables_name>/',views.display_tables, name='display_tables'),
    path('<str:app_name>/<str:tables_name>/<int:obj_id>/change/', views.table_obj_change, name='table_obj_change'), # 修改
    path('<str:app_name>/<str:tables_name>/add', views.table_obj_add, name='table_obj_add'),
]
