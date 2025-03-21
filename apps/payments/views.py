import stripe
import logging
import qrcode
import io
import base64
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.movies.models import Movie, Showtime
from apps.events.models import Event
from apps.bookings.models import Booking  # Import Booking Model
from .models import Payment  # Import Payment Model

logger = logging.getLogger(__name__)  # Logger for debugging

@login_required
def create_checkout_session(request, *args, **kwargs):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Extract IDs from URL kwargs
    movie_id = kwargs.get("movie_id")
    showtime_id = kwargs.get("showtime_id")
    event_id = kwargs.get("event_id")

    # Parse GET parameters
    ticket_count = int(request.GET.get("tickets", 1))
    
    try:
        price_per_ticket = float(request.GET.get("price", 0))
    except (ValueError, TypeError):
        price_per_ticket = 0

    # Log received price to debug
    logger.info(f"🔍 Received price from request: {request.GET.get('price')} (Parsed: {price_per_ticket})")

    line_items = []
    metadata = {"user_id": str(request.user.id)}

    if movie_id and showtime_id:
        # Handle movie payment
        movie = get_object_or_404(Movie, id=movie_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)

        # Force fetch actual price from DB if frontend sends 0 or missing price
        if price_per_ticket <= 0:
            price_per_ticket = getattr(movie, "price", 20)  # Fetch movie price or fallback to 20
            logger.warning(f"⚠️ Using default movie price: {price_per_ticket}")

        # Log final price before creating the session
        logger.info(f"Final Price Per Ticket: {price_per_ticket}")

        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": f"{movie.title} - {showtime.datetime.strftime('%Y-%m-%d %H:%M')}"
                },
                "unit_amount": int(price_per_ticket * 100),  # Convert to pence
            },
            "quantity": ticket_count,
        })

        metadata.update({
            "category": "movie",
            "movie_id": str(movie_id),
            "showtime_id": str(showtime_id),
            "ticket_count": str(ticket_count),
            "price_per_ticket": str(price_per_ticket),
        })

    elif event_id:
        # Handle event payment
        event = get_object_or_404(Event, id=event_id)
        ticket_type = request.GET.get("ticket_type", "General")

        if price_per_ticket <= 0:
            logger.warning(f"No price found for event {event.title}, using 20 GBP default")
            price_per_ticket = 20

        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": f"{event.title} - {ticket_type}"
                },
                "unit_amount": int(price_per_ticket * 100),
            },
            "quantity": ticket_count,
        })

        metadata.update({
            "category": "event",
            "event_id": str(event_id),
            "ticket_type": ticket_type,
            "ticket_count": str(ticket_count),
            "price_per_ticket": str(price_per_ticket),
        })

    else:
        # If neither movie nor event IDs were provided, cancel payment
        return redirect(reverse("payment_cancel"))

    # Log final session details before sending to Stripe
    logger.info(f"🎟️ Creating Stripe session: Tickets: {ticket_count}, Total: {price_per_ticket * ticket_count}")

    # Create the Stripe Checkout Session
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
        logger.error("❌ session_id is missing!")
        return render(request, "payments/success.html", {"error": "Missing session ID"})

    session = stripe.checkout.Session.retrieve(session_id)
    
    # Retrieve metadata
    metadata = session.metadata or {}
    movie_id = metadata.get("movie_id")
    showtime_id = metadata.get("showtime_id")
    event_id = metadata.get("event_id")
    ticket_count = int(metadata.get("ticket_count", 1))
    price_per_ticket = float(metadata.get("price_per_ticket", 0))  
    total_price = ticket_count * price_per_ticket

    movie = get_object_or_404(Movie, id=movie_id) if movie_id else None
    showtime = get_object_or_404(Showtime, id=showtime_id) if showtime_id else None
    event = get_object_or_404(Event, id=event_id) if event_id else None

    # Create Booking
    booking, created = Booking.objects.get_or_create(
        user=request.user,
        movie=movie if movie else None,
        showtime=showtime if showtime else None,
        event=event if event else None,
        defaults={
            "seat_count": ticket_count,
            "total_price": total_price,
            "category": "event" if event else "movie",
        },
    )

    # Generate QR Code
    qr_data = f"""
    Booking Confirmation:
    🎬 Movie: {movie.title if movie else 'N/A'}
    🎟️ Event: {event.title if event else 'N/A'}
    🕒 Showtime: {showtime.datetime if showtime else 'N/A'}
    🎟️ Seats: {ticket_count}
    💰 Total Price: {total_price}
    """
    qr = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_image = buffer.getvalue()

    # Send Email with QR Code attachment
    subject = "🎟️ Your TicketEase Booking Confirmation"
    message = f"""
    Hi {request.user.username},

    Your payment of {total_price} GBP was successful! 🎉

    🎬 {movie.title if movie else 'N/A'}
    🕒 Showtime: {showtime.datetime if showtime else 'N/A'}
    🎟️ Seats: {ticket_count}
    💰 Total Price: {total_price} GBP

    Your QR Code is attached to this email. Please show it at the entrance.

    Thank you for choosing TicketEase!
    
    Best,
    TicketEase Team
    """

    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.attach("booking_qr_code.png", qr_code_image, "image/png")

    try:
        email.send(fail_silently=False)
        logger.info(f"Booking confirmation email sent to {request.user.email}!")
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")

    # Redirect to success page
    return redirect(reverse("booking_success", kwargs={"movie_id": movie_id, "showtime_id": showtime_id}) if movie else reverse("event_success", kwargs={"event_id": event_id}))


@login_required
def payment_cancel(request):
    return render(request, "payments/cancel.html")
