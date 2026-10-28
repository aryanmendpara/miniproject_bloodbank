from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donation
from .forms import DonationForm
from services.donation_service import confirm_donation

@login_required
def donation_list(request):
    donations = Donation.objects.all()
    blood_group = request.GET.get('blood_group')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    if blood_group:
        donations = donations.filter(blood_group=blood_group)
    if status:
        donations = donations.filter(donation_status=status)
    if search:
        donations = donations.filter(donor__full_name__icontains=search) | donations.filter(donation_id__icontains=search)
    
    return render(request, 'donations/donation_list.html', {'donations': donations})

@login_required
def add_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation recorded successfully!')
            return redirect('donation_list')
    else:
        form = DonationForm()
    return render(request, 'donations/add_donation.html', {'form': form})

@login_required
def update_donation_status(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('donation_status')
        if new_status == 'Confirmed' and donation.donation_status != 'Confirmed' and not donation.stock_updated:
            confirm_donation(donation)
            messages.success(request, 'Donation confirmed and stock updated!')
        else:
            donation.donation_status = new_status
            donation.save()
            messages.success(request, 'Donation status updated!')
        return redirect('donation_list')
    return render(request, 'donations/update_status.html', {'donation': donation})
