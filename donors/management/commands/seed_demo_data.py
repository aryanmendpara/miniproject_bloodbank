from django.core.management.base import BaseCommand
from donors.models import Donor
from donations.models import Donation
from inventory.models import BloodInventory, StockMovement
from requests_app.models import BloodRequest
from django.utils import timezone
from datetime import timedelta
import random

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
FIRST_NAMES = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Rohan', 'Kavita', 'Arjun', 'Meera',
               'Sanjay', 'Pooja', 'Karan', 'Neha', 'Aditya', 'Ritika', 'Manish', 'Divya', 'Nikhil', 'Shreya',
               'Rajesh', 'Anita', 'Deepak', 'Swati', 'Varun', 'Isha', 'Mohit', 'Tanvi', 'Suresh', 'Geeta']
LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Gupta', 'Verma', 'Joshi', 'Mehta', 'Nair']
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
CENTERS = ['City Blood Bank', 'Red Cross Center', 'LifeCare Hospital', 'Apollo Blood Bank', 'Metro Blood Center']
HOSPITALS = ['Apollo Hospital', 'Fortis Hospital', 'Max Hospital', 'AIIMS', 'Medanta Hospital', 'Lilavati Hospital']

class Command(BaseCommand):
    help = 'Seed database with demo data for Blood Bank Management System'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')
        
        # Create inventory for all blood groups
        for bg in BLOOD_GROUPS:
            BloodInventory.objects.get_or_create(
                blood_group=bg,
                defaults={'units_available': random.randint(5, 50), 'minimum_threshold': 10}
            )
        
        # Create donors
        for i in range(30):
            donor_id = f'DON{1000+i}'
            if not Donor.objects.filter(donor_id=donor_id).exists():
                Donor.objects.create(
                    donor_id=donor_id,
                    full_name=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
                    age=random.randint(18, 55),
                    gender=random.choice(['Male', 'Female']),
                    blood_group=random.choice(BLOOD_GROUPS),
                    phone_number=f'98765{random.randint(10000, 99999)}',
                    city=random.choice(CITIES),
                    registration_date=timezone.now().date() - timedelta(days=random.randint(30, 500)),
                    last_donation_date=timezone.now().date() - timedelta(days=random.randint(60, 365)) if random.random() > 0.3 else None,
                    donation_eligibility_status=random.choice([True, True, True, False])
                )
        
        # Create donations over last 12 months
        donors = list(Donor.objects.all())
        for i in range(60):
            days_ago = random.randint(0, 365)
            donation_date = timezone.now().date() - timedelta(days=days_ago)
            blood_group = random.choice(BLOOD_GROUPS)
            status = random.choice(['Confirmed', 'Confirmed', 'Confirmed', 'Pending', 'Rejected'])
            units = random.choice([1, 1, 1, 2])
            
            donation_id = f'DONAT{2000+i}'
            if not Donation.objects.filter(donation_id=donation_id).exists():
                donation = Donation.objects.create(
                    donation_id=donation_id,
                    donor=random.choice(donors),
                    blood_group=blood_group,
                    units_collected=units,
                    donation_date=donation_date,
                    collection_center=random.choice(CENTERS),
                    donation_status=status,
                    stock_updated=False
                )
                if status == 'Confirmed':
                    from services.donation_service import confirm_donation
                    confirm_donation(donation)
        
        # Create blood requests
        for i in range(15):
            days_ago = random.randint(0, 180)
            request_date = timezone.now().date() - timedelta(days=days_ago)
            status = random.choice(['Pending', 'Approved', 'Rejected', 'Fulfilled'])
            blood_group = random.choice(BLOOD_GROUPS)
            units = random.choice([1, 2, 3])
            
            request_id = f'REQ{3000+i}'
            if not BloodRequest.objects.filter(request_id=request_id).exists():
                req = BloodRequest.objects.create(
                    request_id=request_id,
                    hospital_name=random.choice(HOSPITALS),
                    blood_group=blood_group,
                    units_requested=units,
                    request_date=request_date,
                    priority=random.choice(['Normal', 'High', 'Emergency']),
                    status=status,
                    stock_updated=False
                )
                if status == 'Fulfilled':
                    from services.request_service import fulfill_request
                    fulfill_request(req)
        
        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
