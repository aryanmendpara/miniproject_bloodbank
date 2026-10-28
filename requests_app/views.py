from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BloodRequest
from .forms import BloodRequestForm
from services.request_service import fulfill_request

@login_required
def request_list(request):
    requests = BloodRequest.objects.all()
    blood_group = request.GET.get('blood_group')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    
    if blood_group:
        requests = requests.filter(blood_group=blood_group)
    if status:
        requests = requests.filter(status=status)
    if priority:
        requests = requests.filter(priority=priority)
    
    return render(request, 'requests/request_list.html', {'requests': requests})

@login_required
def add_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood request submitted successfully!')
            return redirect('request_list')
    else:
        form = BloodRequestForm()
    return render(request, 'requests/add_request.html', {'form': form})

@login_required
def process_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'fulfill' and blood_request.status in ['Pending', 'Approved'] and not blood_request.stock_updated:
            success, msg = fulfill_request(blood_request)
            if success:
                messages.success(request, msg)
            else:
                messages.error(request, msg)
        elif action == 'approve':
            blood_request.status = 'Approved'
            blood_request.save()
            messages.success(request, 'Request approved!')
        elif action == 'reject':
            blood_request.status = 'Rejected'
            blood_request.save()
            messages.success(request, 'Request rejected!')
        return redirect('request_list')
    return render(request, 'requests/process_request.html', {'blood_request': blood_request})
