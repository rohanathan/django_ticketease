from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomSignupForm 
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from apps.notifications.services import notify_user_registration
import logging



logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"✅ New user registered: {user.username}, {user.email}")

            # Debug: Check if function is being called
            print(f"📧 Calling notify_user_registration() for {user.email}")
            logger.info(f"📧 Calling notify_user_registration() for {user.email}")

            notify_user_registration(user)  # Ensure this runs

            print(f"✅ Registration email function executed for {user.email}")
            logger.info(f"✅ Registration email function executed for {user.email}")

            login(request, user)
            messages.success(request, "Registration successful! Check your email for a welcome message.")
            return redirect("home")
        else:
            logger.error("❌ Registration failed due to form validation error.")
            print("❌ Registration failed due to form validation error.")
    else:
        form = CustomSignupForm()
    
    return render(request, "registration/signup.html", {"form": form})


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
    return render(request, "registration/login.html", {"form": form})  # Always return an HTTP response



@login_required
def dashboard(request):
    return render(request, "users/dashboard.html", {"user": request.user})

def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")  # Redirect to dashboard after successful update
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, "Registration successful!")
            return redirect("home")  # Redirect to homepage or dashboard
    else:
        form = UserCreationForm()


def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send welcome email
            #send_notification(
              # user=user,
               # subject="Welcome to TicketEase 🎉",
                # message=f"Hi {user.username},\n\nWelcome to TicketEase! We're excited to have you on board. 🎟️\n\nEnjoy booking events with us!\n\nBest,\nTicketEase Team"
              # )
            login(request, user)
            return redirect("home")  # Redirect to homepage after signup
    else:
        form = CustomSignupForm()
    
    return render(request, "registration/signup.html", {"form": form})


   
