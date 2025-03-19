import qrcode
import io
import base64
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from apps.movies.models import Movie, Showtime, Seat
from django.db.models import Sum



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
    """ Generates QR Code and displays booking confirmation page. """
    selected_seats = request.POST.get("selected_seats", "").split(",")

    # Fetch movie & showtime details
    movie = Movie.objects.get(id=movie_id)
    showtime = Showtime.objects.get(id=showtime_id)

    # Generate QR Code with Booking Details
    qr_data = f"Movie: {movie.title}\nShowtime: {showtime.datetime}\nSeats: {', '.join(selected_seats)}"
    qr = qrcode.make(qr_data)
    
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, "bookings/booking_success.html", {
        "movie": movie,
        "showtime": showtime,
        "selected_seats": selected_seats,
        "qr_code_data": qr_code_data,
    })