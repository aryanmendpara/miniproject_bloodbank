from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from donors.models import Donor
from donations.models import Donation
from inventory.models import BloodInventory
from requests_app.models import BloodRequest
import csv
from datetime import datetime

@login_required
def reports_home(request):
    return render(request, 'reports/reports_home.html')

@login_required
def export_donors_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="donors_{datetime.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Donor ID', 'Full Name', 'Age', 'Gender', 'Blood Group', 'Phone', 'City', 'Registration Date', 'Last Donation', 'Eligible'])
    for donor in Donor.objects.all():
        writer.writerow([donor.donor_id, donor.full_name, donor.age, donor.gender, donor.blood_group, 
                        donor.phone_number, donor.city, donor.registration_date, donor.last_donation_date, 
                        donor.donation_eligibility_status])
    return response

@login_required
def export_donations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="donations_{datetime.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Donation ID', 'Donor', 'Blood Group', 'Units', 'Date', 'Center', 'Status'])
    for donation in Donation.objects.all():
        writer.writerow([donation.donation_id, donation.donor.full_name, donation.blood_group, 
                        donation.units_collected, donation.donation_date, donation.collection_center, 
                        donation.donation_status])
    return response

@login_required
def export_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventory_{datetime.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Blood Group', 'Units Available', 'Minimum Threshold', 'Low Stock'])
    for inv in BloodInventory.objects.all():
        writer.writerow([inv.blood_group, inv.units_available, inv.minimum_threshold, 'Yes' if inv.is_low_stock() else 'No'])
    return response

@login_required
def export_requests_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="requests_{datetime.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Request ID', 'Hospital', 'Blood Group', 'Units', 'Date', 'Priority', 'Status'])
    for req in BloodRequest.objects.all():
        writer.writerow([req.request_id, req.hospital_name, req.blood_group, req.units_requested, 
                        req.request_date, req.priority, req.status])
    return response
