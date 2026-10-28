from django.db import models
from django.utils import timezone

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class Donor(models.Model):
    donor_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    registration_date = models.DateField(default=timezone.now)
    last_donation_date = models.DateField(null=True, blank=True)
    donation_eligibility_status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.donor_id} - {self.full_name} ({self.blood_group})"
    
    class Meta:
        ordering = ['-registration_date']
