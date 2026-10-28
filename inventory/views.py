from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BloodInventory, StockMovement

@login_required
def inventory_list(request):
    inventory = BloodInventory.objects.all().order_by('blood_group')
    return render(request, 'inventory/inventory_list.html', {'inventory': inventory})

@login_required
def stock_movements(request):
    movements = StockMovement.objects.all()
    return render(request, 'inventory/stock_movements.html', {'movements': movements})
