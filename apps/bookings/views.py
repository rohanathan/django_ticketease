import qrcode
import io
import base64
from django.shortcuts import render
from django.http import HttpResponse
from apps.movies.models import Movie, Showtime, Seat
from django.db.models import Sum

def confirm_booking(request, movie_id, showtime_id):
    """ Shows the selected seats for confirmation before proceeding. """
    selected_seats = request.GET.get("seats", "").split(",")

    # Fetch movie & showtime details
    movie = Movie.objects.get(id=movie_id)
    showtime = Showtime.objects.get(id=showtime_id)

    # Calculate total price of selected seats
    total_price = Seat.objects.filter(
        showtime=showtime, 
        row__in=[s[0] for s in selected_seats], 
        number__in=[s[1:] for s in selected_seats]
    ).aggregate(total=Sum('price'))['total'] or 0

    return render(request, "bookings/confirm_booking.html", {
        "movie": movie,
        "showtime": showtime,
        "selected_seats": selected_seats,
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