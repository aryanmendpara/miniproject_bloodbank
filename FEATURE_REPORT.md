# Blood Bank Management System - Feature Report with Code Highlights

## Project Overview

**Project Name:** Blood Bank Management System  
**Technology Stack:** Python, Django 4.2.16, SQLite, HTML5, CSS3, Bootstrap 5, JavaScript, Matplotlib, Tkinter  
**Type:** Web Application + Desktop Utility  
**Purpose:** Educational College Mini Project

---

## 1. Project Structure & Setup

### Key Files
- `manage.py` - Django management script
- `config/` - Project configuration (settings.py, urls.py, wsgi.py)
- `requirements.txt` - All dependencies
- Modular Django apps for separation of concerns

### Code Highlight - Settings Configuration
```python
# config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'donors',
    'donations',
    'inventory',
    'requests_app',
    'dashboard',
    'reports',
]
```

---

## 2. Authentication & Authorization

### Features Implemented
- Django built-in authentication system
- Login/Logout functionality
- Password hashing
- Protected routes using `@login_required`
- CSRF protection
- Staff-only access to admin operations

### Code Highlight - Login View
```python
# config/urls.py
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
```

### Code Highlight - Protected View
```python
# donors/views.py
from django.contrib.auth.decorators import login_required

@login_required
def donor_list(request):
    donors = Donor.objects.all()
    # ... filtering logic
    return render(request, 'donors/donor_list.html', {'donors': donors})
```

---

## 3. Admin Dashboard with Data Visualization

### Features Implemented
- Dynamic summary cards (calculated from database)
- 4 Matplotlib charts (all generated dynamically)
- Real-time statistics

### Summary Cards
- Total registered donors
- Total confirmed donations
- Total available blood units
- Pending blood requests
- Approved requests
- Fulfilled requests
- Low stock groups

### Code Highlight - Dashboard Statistics
```python
# dashboard/views.py
@login_required
def dashboard(request):
    total_donors = Donor.objects.count()
    total_donations = Donation.objects.filter(donation_status='Confirmed').count()
    total_available_units = BloodInventory.objects.aggregate(total=Sum('units_available'))['total'] or 0
    pending_requests = BloodRequest.objects.filter(status='Pending').count()
    approved_requests = BloodRequest.objects.filter(status='Approved').count()
    fulfilled_requests = BloodRequest.objects.filter(status='Fulfilled').count()
    low_stock_groups = BloodInventory.objects.filter(units_available__lt=F('minimum_threshold')).count()
    # ...
```

### Code Highlight - Matplotlib Chart Generation
```python
# dashboard/views.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

def generate_monthly_collection_chart():
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
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    return graphic
```

**Charts Generated:**
1. Monthly Blood Collection (Bar Chart - Last 12 Months)
2. Blood Group Distribution (Pie Chart)
3. Monthly Donation Trends (Line Chart)
4. Blood Inventory Comparison (Bar Chart with color-coded low stock)

---

## 4. Donor Management (Complete CRUD)

### Features Implemented
- Create, Read, Update, Delete donors
- Search by name or donor ID
- Filter by blood group and city
- View donor details with donation history
- Form validation
- Delete confirmation

### Models
```python
# donors/models.py
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
```

### Code Highlight - CRUD Views
```python
# donors/views.py
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
```

---

## 5. Blood Donation Management

### Features Implemented
- Record new donations
- Track donation status (Pending/Confirmed/Rejected)
- Filter by blood group, donor, status, date
- Automatic inventory update on confirmation
- Prevent duplicate stock updates
- View donation history per donor

### Models
```python
# donations/models.py
class Donation(models.Model):
    donation_id = models.CharField(max_length=20, unique=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units_collected = models.IntegerField(default=1)
    donation_date = models.DateField(default=timezone.now)
    collection_center = models.CharField(max_length=200)
    donation_status = models.CharField(max_length=20, choices=DONATION_STATUS_CHOICES, default='Pending')
    stock_updated = models.BooleanField(default=False)
```

### Code Highlight - Donation Service with Transaction
```python
# services/donation_service.py
from django.db import transaction
from inventory.models import BloodInventory, StockMovement

@transaction.atomic
def confirm_donation(donation):
    """
    Confirm a donation and update inventory. Prevent duplicate stock updates.
    """
    if donation.stock_updated:
        return
    
    inventory, created = BloodInventory.objects.get_or_create(
        blood_group=donation.blood_group,
        defaults={'units_available': 0, 'minimum_threshold': 10}
    )
    
    inventory.units_available += donation.units_collected
    inventory.save()
    
    StockMovement.objects.create(
        blood_group=donation.blood_group,
        movement_type='IN',
        quantity=donation.units_collected,
        reason=f"Donation {donation.donation_id} from {donation.donor.full_name}"
    )
    
    donation.donation_status = 'Confirmed'
    donation.stock_updated = True
    donation.save()
```

---

## 6. Blood Inventory Management

### Features Implemented
- Track 8 blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-)
- Real-time stock levels
- Minimum stock threshold configuration
- Low stock alerts (visual indicators)
- Stock movement history (IN/OUT)
- Prevent negative inventory
- Transaction-based updates

### Models
```python
# inventory/models.py
class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, unique=True)
    units_available = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=10)
    
    def is_low_stock(self):
        return self.units_available < self.minimum_threshold

class StockMovement(models.Model):
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
```

### Code Highlight - Inventory Service
```python
# services/inventory_service.py
@transaction.atomic
def deduct_stock(blood_group, quantity, reason):
    """Deduct stock from inventory. Prevent negative inventory."""
    inventory = BloodInventory.objects.get(blood_group=blood_group)
    if inventory.units_available < quantity:
        raise ValueError("Insufficient stock")
    inventory.units_available -= quantity
    inventory.save()
    
    StockMovement.objects.create(
        blood_group=blood_group,
        movement_type='OUT',
        quantity=quantity,
        reason=reason
    )
    return True
```

---

## 7. Blood Request Management

### Features Implemented
- Create blood requests (hospitals/requesters)
- Status tracking (Pending/Approved/Rejected/Fulfilled)
- Priority levels (Normal/High/Emergency)
- Approve/Reject/Fulfill workflow
- Stock availability check before fulfillment
- Automatic stock deduction on fulfillment
- Prevent duplicate deductions
- Transaction management

### Models
```python
# requests_app/models.py
class BloodRequest(models.Model):
    request_id = models.CharField(max_length=20, unique=True)
    hospital_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units_requested = models.IntegerField()
    request_date = models.DateField(default=timezone.now)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    stock_updated = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
```

### Code Highlight - Request Fulfillment with Validation
```python
# services/request_service.py
@transaction.atomic
def fulfill_request(blood_request):
    if blood_request.stock_updated:
        return False, "Request already fulfilled"
    
    try:
        inventory = BloodInventory.objects.get(blood_group=blood_request.blood_group)
    except BloodInventory.DoesNotExist:
        return False, "No inventory found for this blood group"
    
    if inventory.units_available < blood_request.units_requested:
        return False, f"Insufficient stock. Available: {inventory.units_available}, Requested: {blood_request.units_requested}"
    
    try:
        deduct_stock(
            blood_request.blood_group, 
            blood_request.units_requested, 
            f"Request {blood_request.request_id} to {blood_request.hospital_name}"
        )
        blood_request.status = 'Fulfilled'
        blood_request.stock_updated = True
        blood_request.save()
        return True, "Request fulfilled successfully!"
    except ValueError as e:
        return False, str(e)
```

---

## 8. Reports & CSV Export

### Features Implemented
- Donor list export
- Donation history export
- Blood inventory report
- Blood request report
- Protected exports (login required)
- Automatic filenames with timestamps
- Proper CSV headers

### Code Highlight - CSV Export
```python
# reports/views.py
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
```

---

## 9. Dummy Data Seeding

### Features Implemented
- Custom Django management command
- Creates 30 donors with realistic data
- Creates 60 donations distributed over 12 months
- Initializes all 8 blood groups in inventory
- Creates 15 blood requests with mixed statuses
- Auto-confirms donations and fulfills requests
- Safe to run repeatedly (checks for existing records)
- Maintains data consistency

### Code Highlight - Management Command
```python
# donors/management/commands/seed_demo_data.py
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
        
        # Create donors, donations, requests...
        # Auto-process confirmations and fulfillments
        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
```

**Usage:** `python manage.py seed_demo_data`

---

## 10. Modern UI/UX Design

### Features Implemented
- Red, white, and neutral gray color palette
- Fixed top navigation bar with user info
- Sidebar navigation with active states
- Responsive design (Bootstrap 5)
- Dashboard summary cards with icons
- Status badges
- Confirmation modals for destructive actions
- Success/error notifications
- Empty states
- Improved typography with Inter font
- Modern login page with Google/Apple buttons (UI placeholders)
- Forgot password link

### Code Highlight - Enhanced Styling
```css
/* static/css/style.css */
:root {
    --primary-red: #dc2626;
    --primary-red-dark: #b91c1c;
    --bg-light: #f9fafb;
    --border-light: #e5e7eb;
    --text-primary: #111827;
    --text-secondary: #374151;
}

.sidebar {
    position: fixed;
    top: 64px;
    height: calc(100vh - 64px);
    background-color: var(--bg-light) !important;
}

.sidebar .nav-link.active {
    color: white;
    background-color: var(--primary-red);
    font-weight: 600;
}
```

---

## 11. Tkinter Desktop Admin Panel

### Features Implemented
- Standalone desktop application
- Connects directly to SQLite database
- 4 tabs: Dashboard, Donors, Inventory, Blood Requests
- Real-time statistics
- Card-based inventory display with low-stock highlighting
- Data tables for donors and requests
- Refresh functionality
- No impact on web application

### Code Highlight - Tkinter App
```python
# tkinter_admin.py
class BloodBankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System - Desktop Admin")
        self.root.geometry("1000x650")
        self.db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
        
        # Notebook with tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.add(self.dashboard_tab, text="  Dashboard  ")
        self.notebook.add(self.donors_tab, text="  Donors  ")
        self.notebook.add(self.inventory_tab, text="  Inventory  ")
        self.notebook.add(self.requests_tab, text="  Blood Requests  ")
```

**Usage:** `python tkinter_admin.py`

---

## 12. Automated Testing

### Features Implemented
- Django TestCase tests
- Tests for models, services, and business logic
- Coverage for CRUD operations
- Inventory updates testing
- Request fulfillment testing
- Duplicate prevention testing
- Low stock calculations

### Code Highlight - Tests
```python
# tests/test_models.py
class DonationTest(TestCase):
    def test_confirm_donation_updates_inventory(self):
        BloodInventory.objects.create(blood_group='A+', units_available=0)
        confirm_donation(self.donation)
        inv = BloodInventory.objects.get(blood_group='A+')
        self.assertEqual(inv.units_available, 1)
        self.assertTrue(self.donation.stock_updated)

class RequestTest(TestCase):
    def test_fulfill_request(self):
        success, msg = fulfill_request(self.req)
        self.assertTrue(success)
        inv = BloodInventory.objects.get(blood_group='O+')
        self.assertEqual(inv.units_available, 8)
    
    def test_prevent_duplicate_deduction(self):
        fulfill_request(self.req)
        success, msg = fulfill_request(self.req)
        self.assertFalse(success)
```

**Run Tests:** `python manage.py test`

---

## Python Concepts Demonstrated

- **Variables & Data Types** - Throughout all models and views
- **Lists, Tuples, Sets, Dictionaries** - Data structures in views and services
- **Conditional Statements** - Validation logic everywhere
- **Loops (for/while)** - Chart generation, data seeding
- **Functions** - Views, services, helpers
- **Classes & Objects** - Models (OOP), Tkinter GUI class
- **Methods** - Model methods like `is_low_stock()`
- **Exception Handling** - Try/except in services and views
- **List Comprehensions** - Data processing
- **Date & Time Operations** - Using `datetime`, `timezone`
- **File Handling** - CSV generation
- **CSV Module** - Report exports
- **Database Queries & Aggregations** - Django ORM with `Count()`, `Sum()`, `filter()`
- **Transactions** - `@transaction.atomic` in services
- **Object-Relational Mapping** - Django Models

---

## Quick Start Guide

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_demo_data

# Create admin user
python manage.py createsuperuser

# Run web server
python manage.py runserver

# Run desktop app (separate)
python tkinter_admin.py
```

**Access:** http://127.0.0.1:8000/

---

## Repository

**GitHub:** https://github.com/aryanmendpara/miniproject_bloodbank

**Files Count:** 77 Python files, 17 HTML templates

---

*This report highlights all major features and their implementation. The complete working codebase is available in the repository.*


---

## 13. NumPy & Pandas Integration

### Features Implemented
- NumPy arrays used for numerical operations in chart generation
- Pandas DataFrames used for data manipulation and analysis
- Demonstrates Python data science libraries as required

### Code Highlight - NumPy Usage
```python
# dashboard/views.py
import numpy as np
import pandas as pd

# Using numpy for array operations
collections_array = np.array(collections)
plt.bar(months, collections_array, color='#dc3545')

# Using numpy for calculations
sizes_array = np.array(sizes)
plt.pie(sizes_array, labels=labels, autopct='%1.1f%%', startangle=90)
```

### Code Highlight - Pandas Usage
```python
# dashboard/views.py
# Using pandas for data manipulation
trend_df = pd.DataFrame({'Month': months, 'Donations': counts})
plt.plot(trend_df['Month'], trend_df['Donations'], marker='o', color='#dc3545', linewidth=2)

# Using pandas DataFrames for data analysis
donors_df = pd.DataFrame(list(Donor.objects.all().values()))
donations_df = pd.DataFrame(list(Donation.objects.filter(donation_status='Confirmed').values()))
inventory_df = pd.DataFrame(list(BloodInventory.objects.all().values()))
```
