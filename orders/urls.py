from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # Cart
    path("cart/", views.cart_view, name="cart"),
    
    # Add to cart
    path("add/<int:medicine_id>/", views.add_to_cart, name="add_to_cart"),
    path("add-ajax/<int:medicine_id>/", views.add_to_cart_ajax, name="add_to_cart_ajax"),
    
    # Update & remove items
    path("update-quantity/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    
    # Checkout & payment
    path("checkout/", views.checkout_view, name="checkout"),
    path("upi-payment/<int:order_id>/", views.upi_payment_view, name="upi_payment"),
    path("order-success/<int:order_id>/", views.order_success_view, name="order_success"),
]
