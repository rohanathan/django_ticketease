import qrcode
import io
import base64
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from apps.movies.models import Movie, Showtime, Seat
from apps.events.models import Event                
from django.db.models import Sum
from .models import Booking
from django.contrib.auth.decorators import login_required

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
        return redirect(reverse("payment_cancel"))  # Redirect if booking not found

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

    return render(request, "bookings/booking_success.html", {
        "movie": movie,
        "showtime": showtime,
        "seat_count": booking.seat_count,
        "total_price": booking.total_price,
        "qr_code_data": qr_code_data,
        "booking": booking,
    })


def booking_success_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Retrieve the booking record for this user and event.
    booking = Booking.objects.filter(user=request.user, category="event").order_by("-created_at").first()
    if not booking:
        return redirect(reverse("payment_cancel"))
    
    qr_data = f"""
    Booking Confirmation:
    🎟️ Event: {event.title}
    📅 Date: {event.date}
    📍 Location: {event.location}
    Tickets: {booking.seat_count}
    Total Price: {booking.total_price} GBP
    """
    qr = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return render(request, "bookings/booking_success_event.html", {
        "event": event,
        "ticket_count": booking.seat_count,
        "total_price": booking.total_price,
        "qr_code_data": qr_code_data,
        "booking": booking,
    })


@login_required
def my_bookings(request):
    """
    Retrieves all bookings for the logged-in user,
    both movies and events.
    """
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})