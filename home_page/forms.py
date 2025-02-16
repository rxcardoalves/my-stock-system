from django import forms
from .models import StockItem


class AddStockForm(forms.ModelForm):
    """
    A form for adding new stock items.
    """
    class Meta:
        model = StockItem
        fields = ['title', 'description', 'qty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Item Name'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4,
                       'placeholder': 'Item description'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control',
                                            'min': 0,
                                            'placeholder': 'Enter quantity'}),
        }
        labels = {
            'title': 'Stock Title',
            'description': 'Description',
            'qty': 'Quantity',
        }


class EditStockForm(forms.ModelForm):
    """
    A form for editing existing stock items.
    """
    class Meta:
        model = StockItem
        fields = ['title', 'description', 'qty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Item Name'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4,
                       'placeholder': 'Item description'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control',
                                            'min': 0,
                                            'placeholder': 'Enter quantity'}),
        }
        labels = {
            'title': 'Stock Title',
            'description': 'Description',
            'qty': 'Quantity',
        }


class MaintenanceStockForm(forms.ModelForm):
    """
    A form for requesting maintenance on stock items.

    It includes:
    - 'maintenance_quantity': Number of items requiring maintenance.
    - 'maintenance_notes': Details about the maintenance needed.
    """
    class Meta:
        model = StockItem
        fields = ['maintenance_quantity', 'maintenance_notes']
        widgets = {
            'maintenance_quantity': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1}),
            'maintenance_notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4,
                       'placeholder': 'What maintenance is required?'}),
        }

    def save(self, commit=True):
        """
        Overrides save method to update the 'in_maintenance' status.

        If 'maintenance_quantity' is greater than 0, sets
        'in_maintenance' to True. Otherwise, sets it to False.
        """
        instance = super().save(commit=False)

        # Determine if the stock item should be marked as in
        # maintenance.
        if instance.maintenance_quantity > 0:
            instance.in_maintenance = True
        else:
            instance.in_maintenance = False

        if commit:
            instance.save()

        return instance
