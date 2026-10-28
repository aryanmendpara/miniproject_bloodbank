from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from donors.models import Donor
from donations.models import Donation
from inventory.models import BloodInventory
from requests_app.models import BloodRequest
from django.db.models import Sum, Count, F
from datetime import datetime, timedelta
from django.utils import timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

@login_required
def dashboard(request):
    # Summary cards - calculated dynamically
    total_donors = Donor.objects.count()
    total_donations = Donation.objects.filter(donation_status='Confirmed').count()
    
    total_available_units = BloodInventory.objects.aggregate(total=Sum('units_available'))['total'] or 0
    
    pending_requests = BloodRequest.objects.filter(status='Pending').count()
    approved_requests = BloodRequest.objects.filter(status='Approved').count()
    fulfilled_requests = BloodRequest.objects.filter(status='Fulfilled').count()
    
    low_stock_groups = BloodInventory.objects.filter(units_available__lt=F('minimum_threshold')).count()
    
    # Charts
    chart1 = generate_monthly_collection_chart()
    chart2 = generate_blood_group_distribution_chart()
    chart3 = generate_donation_trends_chart()
    chart4 = generate_inventory_comparison_chart()
    
    context = {
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_available_units': total_available_units,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'fulfilled_requests': fulfilled_requests,
        'low_stock_groups': low_stock_groups,
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
    }
    return render(request, 'dashboard/dashboard.html', context)

def generate_monthly_collection_chart():
    # Monthly Blood Collection - last 12 months
    plt.figure(figsize=(8, 4))
    months = []
    collections = []
    for i in range(11, -1, -1):
        date = timezone.now() - timedelta(days=30*i)
        month_name = date.strftime('%b %Y')
        count = Donation.objects.filter(
            donation_status='Confirmed',
            donation_date__year=date.year,
            donation_date__month=date.month
        ).aggregate(total=Sum('units_collected'))['total'] or 0
        months.append(month_name)
        collections.append(count)
    
    plt.bar(months, collections, color='#dc3545')
    plt.title('Monthly Blood Collection (Last 12 Months)')
    plt.xlabel('Month')
    plt.ylabel('Units Collected')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic

def generate_blood_group_distribution_chart():
    plt.figure(figsize=(6, 6))
    inventory = BloodInventory.objects.all()
    labels = [inv.blood_group for inv in inventory]
    sizes = [inv.units_available for inv in inventory]
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Blood Group Distribution (Available Stock)')
    plt.axis('equal')
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic

def generate_donation_trends_chart():
    plt.figure(figsize=(8, 4))
    months = []
    counts = []
    for i in range(11, -1, -1):
        date = timezone.now() - timedelta(days=30*i)
        month_name = date.strftime('%b %Y')
        count = Donation.objects.filter(
            donation_status='Confirmed',
            donation_date__year=date.year,
            donation_date__month=date.month
        ).count()
        months.append(month_name)
        counts.append(count)
    
    plt.plot(months, counts, marker='o', color='#dc3545', linewidth=2)
    plt.title('Monthly Donation Trends')
    plt.xlabel('Month')
    plt.ylabel('Number of Donations')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic

def generate_inventory_comparison_chart():
    plt.figure(figsize=(8, 4))
    inventory = BloodInventory.objects.all().order_by('blood_group')
    groups = [inv.blood_group for inv in inventory]
    units = [inv.units_available for inv in inventory]
    colors = ['#dc3545' if inv.units_available < inv.minimum_threshold else '#28a745' for inv in inventory]
    
    plt.bar(groups, units, color=colors)
    plt.title('Blood Inventory Comparison')
    plt.xlabel('Blood Group')
    plt.ylabel('Units Available')
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic
