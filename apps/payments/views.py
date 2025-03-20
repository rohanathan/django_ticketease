import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Import models for movies and events
from apps.movies.models import Movie, Showtime
from apps.events.models import Event
from .models import Payment  # Payment model in apps/payments/models.py

@login_required
def create_checkout_session(request, *args, **kwargs):
    """
    A single function that handles both movies and events, capturing
    all URL parameters in **kwargs. We'll decide logic based on whether
    'movie_id' or 'event_id' is in kwargs.
    
    Example URL patterns might be:
      - /movies/<int:movie_id>/showtime/<int:showtime_id>/payment/
      - /events/<int:event_id>/create-checkout-session/
    The function won't explicitly accept 'movie_id' or 'event_id' but
    will rely on kwargs.get() to see what's passed.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Extract from kwargs
    movie_id = kwargs.get('movie_id')
    showtime_id = kwargs.get('showtime_id')
    event_id = kwargs.get('event_id')

    # Also parse any GET parameters, e.g. ?tickets=1&price=15
    try:
        ticket_count = int(request.GET.get("tickets", 1))
    except (ValueError, TypeError):
        ticket_count = 1

    try:
        price_per_ticket = float(request.GET.get("price", 0))
    except (ValueError, TypeError):
        price_per_ticket = 0

    line_items = []

    # Decide which domain (movie or event) to handle
    if movie_id and showtime_id:
        # Handle movie
        movie = get_object_or_404(Movie, id=movie_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)

        if price_per_ticket <= 0:
            return redirect(reverse("payment_cancel"))

        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": f"{movie.title} - {showtime.datetime.strftime('%Y-%m-%d %H:%M')}"
                },
                "unit_amount": int(price_per_ticket * 100),
            },
            "quantity": ticket_count,
        })

        metadata = {
            "user_id": request.user.id,
            "category": "movie",
            "movie_id": movie_id,
            "showtime_id": showtime_id,
        }

    elif event_id:
        # Handle event
        event = get_object_or_404(Event, id=event_id)
        # Optionally parse a 'ticket_type' param
        ticket_type = request.GET.get("ticket_type", "General")

        if price_per_ticket <= 0:
            return redirect(reverse("payment_cancel"))

        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event.title} - {ticket_type}"},
                "unit_amount": int(price_per_ticket * 100),
            },
            "quantity": ticket_count,
        })

        metadata = {
            "user_id": request.user.id,
            "category": "event",
            "event_id": event_id,
        }
    else:
        # If neither movie nor event is found, bail out
        return redirect(reverse("payment_cancel"))

    # Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment_success")) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
        metadata=metadata,
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
    payment_email = session.customer_details.email
    registered_email = request.user.email
    recipient_email = payment_email if payment_email else registered_email

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

    # Send Payment Confirmation Email
    if recipient_email:
        subject = "🎟️ TicketEase Payment Confirmation"
        message = f"""
        Hi {request.user.username},

        Your payment of {payment.amount} {payment.currency} was successful! 🎉

        Transaction ID: {payment.transaction_id}
        Amount: {payment.amount} {payment.currency}

        Thank you for using TicketEase!

        Best,
        TicketEase Team
        """
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
            print(f"✅ Payment confirmation email sent to {recipient_email}!")
        except Exception as e:
            print(f"❌ Error sending email: {e}")

    return render(request, "payments/success.html")


@login_required
def payment_cancel(request):
    return render(request, "payments/cancel.html")
