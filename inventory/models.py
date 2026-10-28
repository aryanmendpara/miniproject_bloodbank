from django.db import models
from django.utils import timezone
from donors.models import BLOOD_GROUP_CHOICES

class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, unique=True)
    units_available = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=10)
    
    def __str__(self):
        return f"{self.blood_group}: {self.units_available} units"
    
    def is_low_stock(self):
        return self.units_available < self.minimum_threshold

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]
    
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.movement_type} {self.quantity} units of {self.blood_group}"
    
    class Meta:
        ordering = ['-date']
