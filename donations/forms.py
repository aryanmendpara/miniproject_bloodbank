from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donation_id', 'donor', 'blood_group', 'units_collected', 
                  'donation_date', 'collection_center', 'donation_status']
        widgets = {
            'donation_id': forms.TextInput(attrs={'class': 'form-control'}),
            'donor': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'units_collected': forms.NumberInput(attrs={'class': 'form-control'}),
            'donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'collection_center': forms.TextInput(attrs={'class': 'form-control'}),
            'donation_status': forms.Select(attrs={'class': 'form-control'}),
        }
