from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.notifications.services import notify_user_payment_success
from .models import Payment
#from apps.notifications.utils import send_notification


@login_required
def payment_success(request):
    session_id = request.GET.get("session_id")

    # Fetch the payment object
    payment = Payment.objects.filter(stripe_checkout_id=session_id).first()

    if payment:
        # Update payment status
        payment.status = "success"
        payment.save()

        # Notify user via the notifications app
        notify_user_payment_success(
            user=payment.user,
            transaction_id=payment.transaction_id,
            amount=payment.amount,
            currency=payment.currency
        )

    return render(request, "payments/payment_success.html")
