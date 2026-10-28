from django.test import TestCase
from donors.models import Donor
from donations.models import Donation
from inventory.models import BloodInventory
from requests_app.models import BloodRequest
from django.utils import timezone
from services.donation_service import confirm_donation
from services.request_service import fulfill_request

class DonorModelTest(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(
            donor_id='DON999',
            full_name='Test Donor',
            age=25,
            gender='Male',
            blood_group='O+',
            phone_number='9876543210',
            city='Test City'
        )
    
    def test_donor_creation(self):
        self.assertEqual(self.donor.full_name, 'Test Donor')
        self.assertEqual(self.donor.blood_group, 'O+')

class DonationTest(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(
            donor_id='DON998',
            full_name='Test Donor2',
            age=30,
            gender='Female',
            blood_group='A+',
            phone_number='9876543211',
            city='Test City'
        )
        self.donation = Donation.objects.create(
            donation_id='DONAT999',
            donor=self.donor,
            blood_group='A+',
            units_collected=1,
            donation_date=timezone.now().date(),
            collection_center='Test Center'
        )
    
    def test_donation_creation(self):
        self.assertEqual(self.donation.units_collected, 1)
    
    def test_confirm_donation_updates_inventory(self):
        BloodInventory.objects.create(blood_group='A+', units_available=0)
        confirm_donation(self.donation)
        inv = BloodInventory.objects.get(blood_group='A+')
        self.assertEqual(inv.units_available, 1)
        self.assertTrue(self.donation.stock_updated)

class InventoryTest(TestCase):
    def test_low_stock_calculation(self):
        inv = BloodInventory.objects.create(blood_group='B+', units_available=5, minimum_threshold=10)
        self.assertTrue(inv.is_low_stock())
    
    def test_sufficient_stock(self):
        inv = BloodInventory.objects.create(blood_group='AB+', units_available=20, minimum_threshold=10)
        self.assertFalse(inv.is_low_stock())

class RequestTest(TestCase):
    def setUp(self):
        BloodInventory.objects.create(blood_group='O+', units_available=10)
        self.req = BloodRequest.objects.create(
            request_id='REQ999',
            hospital_name='Test Hospital',
            blood_group='O+',
            units_requested=2,
            request_date=timezone.now().date()
        )
    
    def test_fulfill_request(self):
        success, msg = fulfill_request(self.req)
        self.assertTrue(success)
        inv = BloodInventory.objects.get(blood_group='O+')
        self.assertEqual(inv.units_available, 8)
    
    def test_insufficient_stock(self):
        self.req.units_requested = 20
        self.req.save()
        success, msg = fulfill_request(self.req)
        self.assertFalse(success)
    
    def test_prevent_duplicate_deduction(self):
        fulfill_request(self.req)
        success, msg = fulfill_request(self.req)
        self.assertFalse(success)
        inv = BloodInventory.objects.get(blood_group='O+')
        self.assertEqual(inv.units_available, 8)
