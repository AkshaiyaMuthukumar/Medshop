from django.urls import path
from . import views

app_name = "medicines"

urlpatterns = [
    path('home/', views.home, name='home'),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('', views.all_medicines, name='all_medicines'),
    path('<int:medicine_id>/', views.medicine_detail, name='medicine_detail'),
]
