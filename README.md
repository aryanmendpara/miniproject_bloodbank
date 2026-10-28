# Blood Bank Management System

A complete, functional, beginner-friendly Blood Bank Management System web application built with Python, Django, and Matplotlib for college Python mini project.

## Project Objective

Develop a Blood Bank Management System that allows an administrator to manage blood donors, track blood donations, monitor blood availability, process blood requests, view statistics, and generate reports.

## Features

- **Admin Dashboard** - Modern dashboard with summary cards and 4 Matplotlib charts
- **Donor Management** - Complete CRUD operations with search and filters
- **Blood Donation Management** - Track donations with automatic inventory updates
- **Blood Inventory Management** - Monitor stock for all 8 blood groups with low-stock alerts
- **Blood Request Management** - Process requests with stock validation
- **Reports & CSV Export** - Generate and download reports
- **Admin Authentication** - Secure login with Django authentication
- **Dummy Data Seeding** - Pre-populated data for demonstration

## Technology Stack

- **Python 3.x** - Core programming
- **Django 4.2.16** - Web framework
- **SQLite** - Database
- **HTML5, CSS3, Bootstrap 5** - Frontend
- **JavaScript** - Interactive elements
- **Matplotlib** - Data visualization

## Project Structure

```
blood_bank_management/
├── manage.py
├── requirements.txt
├── README.md
├── config/          # Project settings
├── accounts/        # Authentication
├── donors/          # Donor management
├── donations/       # Donation tracking
├── inventory/       # Inventory management
├── requests_app/    # Blood requests
├── dashboard/       # Admin dashboard
├── reports/         # Reports and exports
├── services/        # Business logic
├── templates/       # HTML templates
├── static/          # CSS, JS, images
└── tests/           # Automated tests
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

#### For macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_demo_data

# Create superuser (admin account)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### For Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_demo_data

# Create superuser (admin account)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Accessing the Application

1. Open your browser and go to `http://127.0.0.1:8000/`
2. Login with the superuser credentials you created
3. You'll be redirected to the admin dashboard

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific tests
python manage.py test tests.test_models
```

## CSV Exports

Navigate to Reports > Export options to download:
- Donor List
- Donation History
- Blood Inventory
- Blood Requests

## Python Concepts Demonstrated

- Variables, data types, lists, tuples, sets, dictionaries
- Conditional statements and loops
- Functions with arguments and return values
- Object-Oriented Programming (Classes and Methods)
- Exception handling
- List comprehensions
- Date and time operations
- File handling and CSV generation
- Django ORM and database queries
- Transactions and business logic
- Data visualization with Matplotlib

## Notes

- This is an educational project for demonstration purposes only
- Do not use in production for actual medical purposes
- All data is fictional
- Uses Django's built-in authentication and security features

## Troubleshooting

**Matplotlib display issues:** The project uses `matplotlib.use('Agg')` for non-interactive backend, which is suitable for web applications.

**Database issues:** If you need to reset, delete `db.sqlite3` and run migrations again.

**Port already in use:** Use `python manage.py runserver 8001` to run on a different port.
