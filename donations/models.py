from django.db import models
from django.utils import timezone
from donors.models import Donor, BLOOD_GROUP_CHOICES

DONATION_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Rejected', 'Rejected'),
]

class Donation(models.Model):
    donation_id = models.CharField(max_length=20, unique=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units_collected = models.IntegerField(default=1)
    donation_date = models.DateField(default=timezone.now)
    collection_center = models.CharField(max_length=200)
    donation_status = models.CharField(max_length=20, choices=DONATION_STATUS_CHOICES, default='Pending')
    stock_updated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.donation_id} - {self.donor.full_name}"
    
    class Meta:
        ordering = ['-donation_date']
