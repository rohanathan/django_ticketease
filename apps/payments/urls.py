from django.urls import path
from .views import create_checkout_session, payment_success, payment_cancel

urlpatterns = [
    path("create-checkout-session/", create_checkout_session, name="create_checkout"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-cancel/", payment_cancel, name="payment_cancel"),
]
