from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm


# -------------------- Register --------------------
def register(request):
    # Redirect logged-in users to home
    if request.user.is_authenticated:
        return redirect('medicines:home')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # auto-login after registration
            messages.success(request, "🎉 Your account has been created and you are now logged in!")
            return redirect('medicines:home')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


# -------------------- Login --------------------
def login(request):
    if request.user.is_authenticated:
        return redirect('medicines:home')

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"✅ Welcome back, {user.email}!")
            return redirect('medicines:home')
        else:
            messages.error(request, "❌ Invalid email or password. Please try again.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "users/login.html", {"form": form})


# -------------------- Logout --------------------
@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "👋 You have been logged out successfully.")
    return redirect("users:login")
