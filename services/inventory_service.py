from django.db import transaction
from inventory.models import BloodInventory, StockMovement

@transaction.atomic
def add_stock(blood_group, quantity, reason):
    """Add stock to inventory"""
    inventory, created = BloodInventory.objects.get_or_create(
        blood_group=blood_group,
        defaults={'units_available': 0, 'minimum_threshold': 10}
    )
    inventory.units_available += quantity
    inventory.save()
    
    StockMovement.objects.create(
        blood_group=blood_group,
        movement_type='IN',
        quantity=quantity,
        reason=reason
    )

@transaction.atomic
def deduct_stock(blood_group, quantity, reason):
    """Deduct stock from inventory. Prevent negative inventory."""
    inventory = BloodInventory.objects.get(blood_group=blood_group)
    if inventory.units_available < quantity:
        raise ValueError("Insufficient stock")
    inventory.units_available -= quantity
    inventory.save()
    
    StockMovement.objects.create(
        blood_group=blood_group,
        movement_type='OUT',
        quantity=quantity,
        reason=reason
    )
    return True
