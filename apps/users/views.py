from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from .forms import CustomSignupForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from apps.notifications.services import notify_user_registration
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

User = get_user_model()  # Using Custom User Model

# Registration View with Success Page Redirect
def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Redirecting you to login...")
            return redirect("registration_success")  # Redirect to success page
    else:
        form = CustomSignupForm()
    
    return render(request, "registration/signup.html", {"form": form})



# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("home")  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


# Dashboard View
@login_required
def dashboard(request):
    return render(request, "users/dashboard.html", {"user": request.user})


# Profile Edit View
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("dashboard")  # Redirect to dashboard after update
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})


# Forgot Password View using Django's Built-in PasswordResetView
class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/forgot_password.html"
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            send_mail(
                "Reset Your Password - TicketEase",
                f"Hi {user.username},\n\nClick the link below to reset your password:\nhttp://127.0.0.1:8000/reset/{user.id}/",
                "noreply@ticketease.com",
                [email],
                fail_silently=False,
            )
        messages.success(self.request, "If an account exists with this email, a reset link has been sent.")
        return super().form_valid(form)

