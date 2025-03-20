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
def create_checkout_session(request, event_id):
    """
    Handles payment for both movies and events via GET request.
    For events, event_id is captured from the URL.
    Expected GET parameters for events:
      - ticket_type (default "General")
      - tickets (number)
      - price (price per ticket)
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Extract required parameters
    category = request.GET.get("category")  # "movie" or "event"
    # For events, use event_id from URL
    item_id = event_id  
    ticket_type = request.GET.get("ticket_type", "General")
    try:
        ticket_count = int(request.GET.get("tickets", 1))
    except (ValueError, TypeError):
        ticket_count = 1

    if not category or not item_id:
        return redirect(reverse("payment_cancel"))

    line_items = []
    total_price = 0

    if category == "movie":
        # Handle Movie Payment
        showtime_id = request.GET.get("showtime_id")
        movie = get_object_or_404(Movie, id=item_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)

        try:
            price_per_ticket = float(request.GET.get("price", 15))
        except (ValueError, TypeError):
            price_per_ticket = 15
        total_price = price_per_ticket * ticket_count

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

    elif category == "event":
        # Handle Event Payment
        event = get_object_or_404(Event, id=item_id)

        # Access ticket_types from the related EventDetail
        # Make sure that every Event has an associated EventDetail instance.
        ticket_types = event.details.ticket_types  # Use the related name "details"
        price_per_ticket = float(ticket_types.get(ticket_type, 0)) if isinstance(ticket_types, dict) else 0

        if price_per_ticket == 0:
            return redirect(reverse("payment_cancel"))

        total_price = price_per_ticket * ticket_count

        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event.title} - {ticket_type} Ticket"},
                "unit_amount": int(price_per_ticket * 100),
            },
            "quantity": ticket_count,
        })
    else:
        return redirect(reverse("payment_cancel"))

    # Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment_success")) + f"?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
        metadata={"user_id": request.user.id, "category": category, "item_id": item_id},
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
