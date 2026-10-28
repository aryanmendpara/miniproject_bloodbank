from django.db import models
from django.utils import timezone
from donors.models import BLOOD_GROUP_CHOICES

PRIORITY_CHOICES = [
    ('Normal', 'Normal'),
    ('High', 'High'),
    ('Emergency', 'Emergency'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Fulfilled', 'Fulfilled'),
]

class BloodRequest(models.Model):
    request_id = models.CharField(max_length=20, unique=True)
    hospital_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units_requested = models.IntegerField()
    request_date = models.DateField(default=timezone.now)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    stock_updated = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.request_id} - {self.hospital_name} ({self.blood_group})"
    
    class Meta:
        ordering = ['-request_date']
