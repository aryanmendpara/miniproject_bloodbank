from django.db import transaction
from inventory.models import BloodInventory, StockMovement

@transaction.atomic
def confirm_donation(donation):
    """
    Confirm a donation and update inventory. Prevent duplicate stock updates.
    Demonstrates transaction management and business logic.
    """
    if donation.stock_updated:
        return
    
    inventory, created = BloodInventory.objects.get_or_create(
        blood_group=donation.blood_group,
        defaults={'units_available': 0, 'minimum_threshold': 10}
    )
    
    inventory.units_available += donation.units_collected
    inventory.save()
    
    StockMovement.objects.create(
        blood_group=donation.blood_group,
        movement_type='IN',
        quantity=donation.units_collected,
        reason=f"Donation {donation.donation_id} from {donation.donor.full_name}"
    )
    
    donation.donation_status = 'Confirmed'
    donation.stock_updated = True
    donation.save()
