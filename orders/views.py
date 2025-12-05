from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum, F
from django.http import JsonResponse
from .models import Order, OrderItem
from medicines.models import Medicine

# -------------------------
# Helper function to get cart count
def get_cart_count(user):
    """Returns total items in cart for the user."""
    if user.is_authenticated:
        order = Order.objects.filter(user=user, is_ordered=False).first()
        if order:
            return order.items.aggregate(total=Sum('quantity'))['total'] or 0
    return 0

# -------------------------
# CART VIEW
def cart_view(request):
    """Show cart items. If not logged in, show a friendly message and redirect."""
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to view your cart.")
        return redirect(settings.LOGIN_URL)

    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    items = order.items.all()
    total = items.aggregate(total_price=Sum(F('quantity') * F('medicine__price')))['total_price'] or 0

    return render(request, 'orders/cart.html', {
        'order': order,
        'items': items,
        'total': total
    })

# -------------------------
# ADD TO CART (Normal)
def add_to_cart(request, medicine_id):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to add items to cart.")
        return redirect(settings.LOGIN_URL)
    
    medicine = get_object_or_404(Medicine, id=medicine_id)
    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, medicine=medicine)

    if not created:
        order_item.quantity = F('quantity') + 1
        order_item.save()
        order_item.refresh_from_db()
    else:
        order_item.quantity = 1
        order_item.save()

    messages.success(request, f"{medicine.name} added to cart successfully!")

    # AJAX support
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_items = order.items.aggregate(total=Sum('quantity'))['total'] or 0
        return JsonResponse({
            'success': True,
            'medicine_name': medicine.name,
            'total_items': total_items
        })

    return redirect(request.META.get('HTTP_REFERER', 'medicines:home'))

# -------------------------
# ADD TO CART AJAX
def add_to_cart_ajax(request, medicine_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': '⚠️ Please login first.'}, status=403)
    
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        medicine = get_object_or_404(Medicine, id=medicine_id)
        order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, medicine=medicine)

        if not created:
            order_item.quantity = F('quantity') + 1
            order_item.save()
            order_item.refresh_from_db()
        else:
            order_item.quantity = 1
            order_item.save()

        total_items = order.items.aggregate(total=Sum('quantity'))['total'] or 0

        return JsonResponse({
            'success': True,
            'medicine_name': medicine.name,
            'total_items': total_items
        })
    return JsonResponse({'success': False}, status=400)

# -------------------------
# UPDATE QUANTITY (+ / -)
def update_quantity(request, item_id):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to update cart items.")
        return redirect(settings.LOGIN_URL)

    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_ordered=False)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        item.save()
    
    return redirect('orders:cart')

# -------------------------
# REMOVE FROM CART
def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to remove cart items.")
        return redirect(settings.LOGIN_URL)
    
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_ordered=False)
    order_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('orders:cart')

# -------------------------
# CHECKOUT
def checkout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to proceed to checkout.")
        return redirect(settings.LOGIN_URL)
    
    order = get_object_or_404(Order, user=request.user, is_ordered=False)
    total_price = order.items.aggregate(total_price=Sum(F('quantity') * F('medicine__price')))['total_price'] or 0

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment')

        order.full_name = full_name
        order.address = address
        order.phone = phone
        order.payment_method = payment_method
        order.save()

        if payment_method == "UPI":
            return redirect('orders:upi_payment', order_id=order.id)
        else:
            order.is_ordered = True
            order.save()
            return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'order': order,
        'total_price': total_price
    })

# -------------------------
# UPI PAYMENT
def upi_payment_view(request, order_id):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to complete payment.")
        return redirect(settings.LOGIN_URL)

    order = get_object_or_404(Order, id=order_id, user=request.user, is_ordered=False)
    total_price = order.items.aggregate(total_price=Sum(F('quantity') * F('medicine__price')))['total_price'] or 0

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        order.transaction_id = transaction_id
        order.is_ordered = True
        order.save()
        messages.success(request, "Payment successful!")
        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/upi_payment.html', {
        'order': order,
        'total_price': total_price
    })

# -------------------------
# ORDER SUCCESS
def order_success_view(request, order_id):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Please login first to view your orders.")
        return redirect(settings.LOGIN_URL)

    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})
