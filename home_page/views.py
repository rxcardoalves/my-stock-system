from django.shortcuts import render, get_object_or_404, redirect
from .models import StockItem
from .forms import AddStockForm, EditStockForm, MaintenanceStockForm

# Create your views here.


def index(request):
    """
    View to display the list of stock items that are not in maintenance.
    """
    stock_list = StockItem.objects.filter(in_maintenance=False
                                          ).order_by('title')
    context = {'stock_list': stock_list}
    return render(request, "index.html", context)


def add_stock(request):
    """
    A view for adding a new stock item.
    """
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            stock_item = form.save(commit=False)
            stock_item.user = request.user  # Assign logged-in user.
            stock_item.save()
            return redirect('/')
    else:
        form = AddStockForm()

    return render(request, 'add_stock.html', {'form': form})


def edit_stock(request, pk):
    """
    A view for editing stock items.
    """
    stock_item = get_object_or_404(StockItem, pk=pk)

    if request.method == 'POST':
        form = EditStockForm(request.POST, instance=stock_item)
        if form.is_valid():
            stock_item = form.save(commit=False)

            stock_item.save()
            return redirect('stock-index')  # Redirect to stock index, or wherever
    else:
        form = EditStockForm(instance=stock_item)

    return render(request, 'edit_stock.html',
                  {'form': form, 'stock_item': stock_item})


def add_to_maintenance(request, pk):
    """
    A view for updating stock items that require maintenance.
    """
    stock_item = get_object_or_404(StockItem, pk=pk)

    if request.method == 'POST':
        form = MaintenanceStockForm(request.POST, instance=stock_item)

        if form.is_valid():
            maintenance_quantity = form.cleaned_data['maintenance_quantity']
            maintenance_notes = form.cleaned_data['maintenance_notes']

            # Ensure maintenance quantity does not exceed stock
            # quantity.
            if maintenance_quantity > stock_item.qty:
                form.add_error('maintenance_quantity', (
                    'Maintenance quantity cannot exceed available stock.'))
            else:
                # Update maintenance details.
                stock_item.maintenance_quantity = maintenance_quantity
                stock_item.maintenance_notes = maintenance_notes
                stock_item.in_maintenance = maintenance_quantity > 0
                stock_item.save()

            return redirect('maintenance_list')
    else:
        form = MaintenanceStockForm(instance=stock_item)

    return render(request, 'maintenance_detail.html', {
        'form': form,
        'stock_item': stock_item,
        'current_qty': stock_item.qty,
        'current_maintenance_qty': stock_item.maintenance_quantity,
        'current_maintenance_notes': stock_item.maintenance_notes})


def maintenance_detail(request, pk):
    """
    A view displaying details of a stock item in maintenance.
    Handles updates to maintenance details.
    """
    stock_item = get_object_or_404(StockItem, pk=pk)

    if request.method == 'POST':
        form = MaintenanceStockForm(request.POST, instance=stock_item)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')  # Redirect after update.
        form = MaintenanceStockForm(instance=stock_item)

    return render(request, 'maintenance_detail.html', {
        'form': form, 'stock_item': stock_item
    })


def maintenance_list(request):
    """
    A view displaying all stock items currently in maintenance.
    """
    # Filter only items where 'in_maintenance' is True
    maintenance_list = StockItem.objects.filter(
        in_maintenance=True).order_by('title')

    context = {'maintenance_list': maintenance_list}
    return render(request, "maintenance_list.html", context)
