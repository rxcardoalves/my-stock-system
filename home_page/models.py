from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class StockItem(models.Model):
    """
    A model representing a stock item and its details.

    Attributes:
        title (str): The name of the stock item (max 140 characters).
        description (str): A brief description of the stock item
        (max 500 characters).
        qty (int): The total quantity of the stock item available.
        user (User): The user who last modified the stock item.
        date (datetime): The timestamp of the last update.
        in_maintenance (bool): Indicates if the stock item is currently
        under maintenance.
        maintenance_quantity (int): The number of items set aside for
        maintenance.
        maintenance_notes (str): Additional notes about the maintenance
        process.

    Methods:
        available_stock(): Returns the number of stock items available
        for use.
        __str__(): Returns a string representation of the stock item.
    """
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=500)
    qty = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)

    in_maintenance = models.BooleanField(default=False)
    maintenance_quantity = models.PositiveIntegerField(default=0)
    maintenance_notes = models.TextField(null=True, blank=True, default="")

    def available_stock(self):
        """
        Calculates the available stock by subtracting the maintenance
        quantity from the total stock quantity.
        """
        return self.qty - self.maintenance_quantity

    def __str__(self):
        """
        Returns a string representation of the stock item, including its
        title, description, and stock quantity.
        """
        return f"{self.title} - {self.description} (In Stock: {self.qty})"
