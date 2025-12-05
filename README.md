MedShop

Features
✅Browse medical products
✅Add to cart & checkout
✅UPI QR Code payment
✅Enter transaction ID
✅Admin can manage products & orders

How to Run
✅pip install -r requirements.txt
✅python manage.py migrate
✅python manage.py runserver

Folder Structure
✅products/      → Product features
✅orders/        → Cart & payment
✅templates/     → HTML files
✅static/        → CSS, JS, images
✅media/         → Uploaded images

Prerequisites

Python 3.8+
Django installed

2. DETAILED TECHNICAL README 

MedShop – Online Medicine Store

Features
✅User-friendly product browsing
✅Dynamic cart & quantity updates
✅Checkout with price calculation
✅Auto-generated UPI QR code
✅Transaction ID submission
✅Admin dashboard for product & order management

How to Run

✅Install dependencies:
pip install -r requirements.txt

✅Apply database migrations:
python manage.py migrate

✅Start development server:
python manage.py runserver

✅Access the site at:
http://localhost:8000

Folder Structure
medshop/          → Django project settings
products/         → Product CRUD & pages
orders/           → Cart, checkout, UPI payment
templates/        → Base HTML, product pages, checkout UI
static/           → CSS, JS, product images
media/            → Uploaded product images (admin)
requirements.txt  → Project dependencies

Prerequisites

✅Python 3.8 or higher
✅Django installed
✅Internet connection for QR code API
Optional: Admin account for backend access

3. DEPLOYMENT-READY README 
MedShop – Django E-Commerce App

Features
✅Product listing & searching
✅Add to cart, update, and remove items
✅Checkout + total amount calculation
✅UPI QR Code generation
✅Transaction ID verification
✅Complete admin panel for products & orders

How to Run Locally
1. Setup Environment
python -m venv env
env\Scripts\activate
pip install -r requirements.txt

2. Setup Database
python manage.py migrate

3. Run the Server
python manage.py runserver

Folder Structure
medshop/              → Core settings, URLs
products/             → Products app
orders/               → Orders + payments
templates/            → HTML templates
static/               → CSS/JS assets
media/                → Uploaded images

Prerequisites
✅Python 3.8+
✅Django 4+
✅Render / Railway / PythonAnywhere (for deployment)
