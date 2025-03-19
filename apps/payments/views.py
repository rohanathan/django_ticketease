import stripe
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # Import email function
from apps.movies.models import Movie, Showtime
from apps.events.models import Event  # ✅ Import Event Model
from apps.payments.models import Payment

@login_required
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    category = request.GET.get("category")  # ✅ Is it a movie or event?
    seat_count = int(request.GET.get("seats", 1)) if category == "movie" else int(request.GET.get("tickets", 1))

    if category == "movie":
        # ✅ Movie Payment Logic
        movie_id = request.GET.get("movie_id")
        showtime_id = request.GET.get("showtime_id")
        movie = get_object_or_404(Movie, id=movie_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)
        price_per_ticket = 200  # ₹200 per seat (Modify if needed)
        total_price = seat_count * price_per_ticket
        description = f"{movie.title} - {showtime.datetime.strftime('%Y-%m-%d %H:%M')}"

    elif category == "event":
        # ✅ Event Payment Logic
        event_id = request.GET.get("event_id")
        event = get_object_or_404(Event, id=event_id)
        price_per_ticket = event.price  # Use event's price dynamically
        total_price = seat_count * price_per_ticket
        description = f"Event: {event.title} - {event.date.strftime('%Y-%m-%d')}"

    else:
        return render(request, "payments/error.html", {"error": "Invalid payment category."})

    # ✅ Convert to smallest currency unit for Stripe
    total_price_cents = total_price * 100

    # ✅ Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': description},
                    'unit_amount': total_price_cents,
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')) + f"?session_id={{CHECKOUT_SESSION_ID}}&category={category}",
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        metadata={"user_id": request.user.id, "category": category},
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
