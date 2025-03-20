import qrcode
import io
import base64
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from apps.movies.models import Movie, Showtime, Seat
from django.db.models import Sum
from .models import Booking

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
