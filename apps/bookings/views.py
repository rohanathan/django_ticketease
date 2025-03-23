import qrcode
import io
import base64
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from apps.movies.models import Movie, Showtime, Seat
from apps.events.models import Event                
from django.db.models import Sum, Q
from .models import Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.notifications.services import notify_user_booking_cancelled


def confirm_booking(request, movie_id, showtime_id):
    """ Show booking summary based on the number of seats selected. """
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)

    # Get seat count from URL parameters
    seat_count = int(request.GET.get("seats", 1))

    # Assume fixed pricing per seat (Modify if needed)
    price_per_seat = 200  # Example price (₹200 per seat)
    total_price = seat_count * price_per_seat

    return render(request, "bookings/confirm_booking.html", {
        "movie": movie,
        "showtime": showtime,
        "seat_count": seat_count,
        "total_price": total_price

    })



def booking_success(request, movie_id, showtime_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)

    # Ensure we fetch the correct booking
    booking = Booking.objects.filter(
        user=request.user, movie=movie, showtime=showtime
    ).order_by("-created_at").first()

    if not booking:
        return redirect(reverse("payment_cancel"))

    # Generate QR Code again
    qr_data = f"""
    Booking Confirmation:
    🎬 Movie: {movie.title}
    🕒 Showtime: {showtime.datetime}
    🎟️ Seats: {booking.seat_count}
    💰 Total Price: {booking.total_price}
    """
    qr = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    from django.utils.timezone import now
    is_upcoming = showtime.datetime > now()

    from_dashboard = request.GET.get("from_dashboard") == "1"

    return render(request, "bookings/booking_success.html", {
        "from_dashboard": from_dashboard,
        "movie": movie,
        "showtime": showtime,
        "seat_count": booking.seat_count,
        "total_price": booking.total_price,
        "qr_code_data": qr_code_data,
        "booking": booking,
        "is_upcoming": is_upcoming,
    })



def booking_success_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    booking = Booking.objects.filter(user=request.user, event=event).order_by("-created_at").first()

    if not booking:
        return redirect(reverse("payment_cancel"))

    # Generate QR Code
    qr_data = f"""
    Booking Confirmation:
    🎤 Event: {event.title}
    📅 Date: {event.date}
    📍 Location: {event.location}
    🎟️ Tickets: {booking.seat_count}
    💰 Total Price: {booking.total_price}
    """
    qr = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    from django.utils.timezone import now
    is_upcoming = event.date > now().date()

    from_dashboard = request.GET.get("from_dashboard") == "1"

    return render(request, "bookings/booking_success_event.html", {
        "from_dashboard": from_dashboard,
        "event": event,
        "booking": booking,
        "qr_code_data": qr_code_data,
        "is_upcoming": is_upcoming,
    })

@login_required
def my_bookings(request):
    """Displays upcoming and past bookings separately like homepage layout."""

    now_time = now()

    # Only confirmed & future = upcoming
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        status='confirmed'
    ).filter(
        (Q(category="movie") & Q(showtime__datetime__gte=now_time)) |
        (Q(category="event") & Q(event__date__gte=now_time.date()))
    ).order_by("created_at")

    # Everything else = past (includes cancelled and expired)
    past_bookings = Booking.objects.filter(user=request.user).exclude(
        id__in=upcoming_bookings.values_list('id', flat=True)
    ).order_by("-created_at")

    return render(request, "bookings/my_bookings.html", {
        "upcoming_bookings": upcoming_bookings,
        "past_bookings": past_bookings
    })


@require_POST
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == 'cancelled':
        messages.warning(request, "This booking has already been cancelled.")
        return redirect('my_bookings')

    # Mark as cancelled
    booking.status = 'cancelled'
    booking.save()

    # Trigger email confirmation
    notify_user_booking_cancelled(request.user, booking)

    messages.success(request, "Booking cancelled successfully. Refund will be processed in 5–7 business days.")
    return redirect('my_bookings')