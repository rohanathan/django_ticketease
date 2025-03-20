from django.urls import path
from .views import signup_view, login_view, dashboard, edit_profile, CustomPasswordResetView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", signup_view, name="signup"),  # Keeping signup as is
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("edit-profile/", edit_profile, name="edit_profile"),

    # Forgot Password URLs
    path("forgot-password/", CustomPasswordResetView.as_view(), name="forgot_password"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

    # Registration Success Page
    path("registration-success/", TemplateView.as_view(template_name="registration/registration_success.html"), name="registration_success"),
]
