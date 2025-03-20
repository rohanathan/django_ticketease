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
def create_checkout_session(request, movie_id, showtime_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    category = request.GET.get("category", "movie")  # Default category is movie
    seat_count = int(request.GET.get("tickets", 1))  # Number of tickets
    price_per_ticket = int(request.GET.get("price", 15))  # Assume £15 per ticket

    # ✅ Fetch movie & showtime details
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)

    total_price = seat_count * price_per_ticket  # Calculate total

    # ✅ Convert total price to pence (Stripe uses the smallest currency unit)
    total_price_pence = total_price * 100  # £1 = 100 pence

    # ✅ Create Stripe Checkout Session with GBP
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'gbp',  # ✅ Use GBP instead of INR
                    'product_data': {'name': f"{movie.title} - {showtime.datetime.strftime('%Y-%m-%d %H:%M')}"},
                    'unit_amount': total_price_pence,  # Amount in pence
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')) + f"?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        metadata={"user_id": request.user.id, "movie_id": movie_id, "showtime_id": showtime_id},
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
