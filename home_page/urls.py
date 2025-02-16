from django.urls import path
from django.views.generic import ListView
from .models import StockItem
from . import views

urlpatterns = [
    # URL pattern for the Stock index page.
    path('', ListView.as_view(
        model=StockItem,
        template_name="index.html",
        context_object_name="stock_list",
        ordering=['title'],
    ), name='stock-index'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('edit_stock/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('maintenance_list/', views.maintenance_list, name='maintenance_list'),
    path('maintenance_detail/<int:pk>/', views.maintenance_detail,
         name='maintenance_detail'),
    path('add_to_maintenance/<int:pk>/', views.add_to_maintenance,
         name='add_to_maintenance'),
]
