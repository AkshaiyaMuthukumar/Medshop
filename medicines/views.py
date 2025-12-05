from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Medicine
from orders.views import get_cart_count  # Import the helper function

# -------------------------
# Home page: shows latest 8 medicines
def home(request):
    medicines = Medicine.objects.all()[:8]
    cart_count = get_cart_count(request.user)
    return render(request, 'medicines/home.html', {
        'medicines': medicines,
        'cart_count': cart_count
    })

# -------------------------
# All medicines page with optional category filter and pagination
def all_medicines(request):
    category = request.GET.get('category')
    if category:
        medicines_list = Medicine.objects.filter(category=category)
    else:
        medicines_list = Medicine.objects.all()

    paginator = Paginator(medicines_list, 12)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)

    cart_count = get_cart_count(request.user)
    return render(request, 'medicines/all_medicines.html', {
        'medicines': medicines,
        'cart_count': cart_count
    })

# -------------------------
# Medicine detail page
def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart_count = get_cart_count(request.user)
    return render(request, 'medicines/medicine_detail.html', {
        'medicine': medicine,
        'cart_count': cart_count
    })

# -------------------------
# About page
def about(request):
    cart_count = get_cart_count(request.user)
    return render(request, "medicines/about.html", {'cart_count': cart_count})

# -------------------------
# Contact page
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        messages.success(request, "Thank you for contacting us! We will get back to you soon.")
        return redirect("medicines:contact")

    cart_count = get_cart_count(request.user)
    return render(request, "medicines/contact.html", {'cart_count': cart_count})
