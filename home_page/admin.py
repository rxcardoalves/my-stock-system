from django.contrib import admin
from .models import StockItem

# Allows the StockItem model to be managed through the Django admin
# interface.
admin.site.register(StockItem)
