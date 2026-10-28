from django.db import transaction
from inventory.models import BloodInventory
from services.inventory_service import deduct_stock

@transaction.atomic
def fulfill_request(blood_request):
    """
    Fulfill blood request with stock checking and deduction.
    Prevents duplicate deductions.
    """
    if blood_request.stock_updated:
        return False, "Request already fulfilled"
    
    try:
        inventory = BloodInventory.objects.get(blood_group=blood_request.blood_group)
    except BloodInventory.DoesNotExist:
        return False, "No inventory found for this blood group"
    
    if inventory.units_available < blood_request.units_requested:
        return False, f"Insufficient stock. Available: {inventory.units_available}, Requested: {blood_request.units_requested}"
    
    try:
        deduct_stock(
            blood_request.blood_group, 
            blood_request.units_requested, 
            f"Request {blood_request.request_id} to {blood_request.hospital_name}"
        )
        blood_request.status = 'Fulfilled'
        blood_request.stock_updated = True
        blood_request.save()
        return True, "Request fulfilled successfully!"
    except ValueError as e:
        return False, str(e)
