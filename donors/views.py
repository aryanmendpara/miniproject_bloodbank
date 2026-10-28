from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donor
from .forms import DonorForm
from donations.models import Donation

@login_required
def donor_list(request):
    donors = Donor.objects.all()
    blood_group = request.GET.get('blood_group')
    city = request.GET.get('city')
    search = request.GET.get('search')
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    if city:
        donors = donors.filter(city__icontains=city)
    if search:
        donors = donors.filter(full_name__icontains=search) | donors.filter(donor_id__icontains=search)
    
    return render(request, 'donors/donor_list.html', {'donors': donors})

@login_required
def add_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor registered successfully!')
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'donors/add_donor.html', {'form': form})

@login_required
def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    donations = Donation.objects.filter(donor=donor).order_by('-donation_date')
    return render(request, 'donors/donor_detail.html', {'donor': donor, 'donations': donations})

@login_required
def edit_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor updated successfully!')
            return redirect('donor_detail', pk=donor.pk)
    else:
        form = DonorForm(instance=donor)
    return render(request, 'donors/edit_donor.html', {'form': form, 'donor': donor})

@login_required
def delete_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Donor deleted successfully!')
        return redirect('donor_list')
    return render(request, 'donors/delete_donor.html', {'donor': donor})
