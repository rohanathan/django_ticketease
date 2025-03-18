from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.notifications.services import notify_user_payment_success
from .models import Payment
import logging

logger = logging.getLogger(__name__)

@login_required
def payment_success(request):
    session_id = request.GET.get("session_id")
    logger.info(f"🛒 Payment successful, checking session_id: {session_id}")

    # Fetch the payment object
    payment = Payment.objects.filter(stripe_checkout_id=session_id).first()

    if payment:
        logger.info(f"✅ Payment found: {payment.transaction_id}, User: {payment.user.username}")

        # Update payment status
        payment.status = "success"
        payment.save()

        # Notify user via email
        notify_user_payment_success(
            user=payment.user,
            transaction_id=payment.transaction_id,
            amount=payment.amount,
            currency=payment.currency,
            payment_email=payment.user.email  # Ensure this is passed correctly
        )
    else:
        logger.error(f"❌ Payment not found for session ID: {session_id}")

    return render(request, "payments/payment_success.html")
