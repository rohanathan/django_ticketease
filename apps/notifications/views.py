from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.notifications.services import notify_user_payment_success
from .models import Payment
import logging
import stripe
from django.conf import settings
from django.urls import reverse


logger = logging.getLogger(__name__)

@login_required
def payment_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get("session_id")

    if not session_id:
        print("❌ session_id is missing!")
        return render(request, "payments/success.html", {"error": "Missing session ID"})

    session = stripe.checkout.Session.retrieve(session_id)
    
    # Retrieve metadata from the session
    metadata = session.metadata  # This should be a dict with our IDs
    movie_id = metadata.get("movie_id")
    showtime_id = metadata.get("showtime_id")
    # (For events you might use event_id)

    print(f"Stripe Session Retrieved: {session}")

    # Save payment details in the database
    payment = Payment.objects.create(
        user=request.user,
        transaction_id=session.id,
        stripe_checkout_id=session.id,
        amount=session.amount_total / 100,
        currency=session.currency.upper(),
        status="success" if session.payment_status == "paid" else "failed",
    )

    print(f"Payment Saved: {payment}")

    # Pass the IDs to the template so that reverse() can work
    context = {
        "payment": payment,
        "movie_id": movie_id,
        "showtime_id": showtime_id,
    }

    return render(request, "payments/success.html", context)