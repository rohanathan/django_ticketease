import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.movies.models import Movie, Showtime
from apps.events.models import Event



@login_required
def create_checkout_session(request):
    """ Handles payment for both movies & events via GET request """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # ✅ Extract required parameters from GET request
    category = request.GET.get("category")  # "movie" or "event"
    item_id = request.GET.get("id")  # Movie ID or Event ID
    ticket_type = request.GET.get("ticket_type", "General")  # Default to "General"
    ticket_count = int(request.GET.get("tickets", 1))

    if not category or not item_id:
        return redirect(reverse("payment_cancel"))  # Redirect to cancel page

    line_items = []
    total_price = 0

    # ✅ **Handle Movie Payment**
    if category == "movie":
        showtime_id = request.GET.get("showtime_id")
        movie = get_object_or_404(Movie, id=item_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)

        price_per_ticket = float(request.GET.get("price", 15))  # Default £15
        total_price = price_per_ticket * ticket_count

        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{movie.title} - {showtime.datetime.strftime('%Y-%m-%d %H:%M')}"},
                "unit_amount": int(price_per_ticket * 100),  # Convert to pence
            },
            "quantity": ticket_count,
        })

    # ✅ **Handle Event Payment**
    elif category == "event":
        event = get_object_or_404(Event, id=item_id)

        # 🔧 FIX: Retrieve ticket prices correctly
        ticket_types = event.ticket_types  # Ensure this is a JSONField
        price_per_ticket = float(ticket_types.get(ticket_type, 0)) if isinstance(ticket_types, dict) else 0

        if price_per_ticket == 0:
            return redirect(reverse("payment_cancel"))


        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event.title} - {ticket_type}"},
                "unit_amount": int(price_per_ticket * 100),
            },
            "quantity": ticket_count,
        })

    # ✅ **Create Stripe Checkout Session**
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment_success")) + f"?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
        metadata={"user_id": request.user.id, "category": category, "item_id": item_id},
    )

    return redirect(checkout_session.url)  # ✅ **Redirect to Stripe Checkout**





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
