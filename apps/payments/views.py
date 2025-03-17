import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # Import email function
from .models import Payment  # Import Payment model


@login_required
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'TicketEase Event Ticket',
                    },
                    'unit_amount': 2000,  # Amount in cents ($20.00)
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        metadata={"user_id": request.user.id},  # Store user ID in metadata
    )

    return redirect(checkout_session.url)


@login_required
def payment_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get("session_id")

    if not session_id:
        print("❌ session_id is missing!")
        return render(request, "payments/success.html", {"error": "Missing session ID"})

    session = stripe.checkout.Session.retrieve(session_id)
    
    # Retrieve email details
    payment_email = session.customer_details.email  # Email entered during payment
    registered_email = request.user.email  # Registered email in your system
    recipient_email = payment_email if payment_email else registered_email  # Prioritize payment email

    print(f"✅ Stripe Session Retrieved: {session}")

    # Save payment details in the database
    payment = Payment.objects.create(
        user=request.user,
        transaction_id=session.id,
        stripe_checkout_id=session.id,
        amount=session.amount_total / 100,
        currency=session.currency.upper(),
        status="success" if session.payment_status == "paid" else "failed",
    )

    print(f"✅ Payment Saved: {payment}")

    # **Send Payment Confirmation Email**
    if recipient_email:
        subject = "🎟️ TicketEase Payment Confirmation"
        message = f"""
        Hi {request.user.username},

        Your payment of {payment.amount} {payment.currency} was successful! 🎉

        **Transaction ID:** {payment.transaction_id}
        **Amount:** {payment.amount} {payment.currency}

        Thank you for using TicketEase!

        Best,
        TicketEase Team
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Sender email
                [recipient_email],  # Prioritize payment email, fallback to registered email
                fail_silently=False,
            )
            print(f"✅ Payment confirmation email sent to {recipient_email}!")
        except Exception as e:
            print(f"❌ Error sending email: {e}")

    return render(request, "payments/success.html")


@login_required
def payment_cancel(request):
    return render(request, "payments/cancel.html")
