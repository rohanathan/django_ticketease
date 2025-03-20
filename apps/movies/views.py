from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Movie, Showtime, Venue
from datetime import datetime
from datetime import date  # ✅ FIX: Import date

# List all movies
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

# Movie detail page
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    venues = Venue.objects.all()  # ✅ Fetch all venues
    today = date.today()  # ✅ Send today's date for date picker

    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "venues": venues,  # ✅ Ensure venues are passed
        "today": today
    })

#Seat selection
def select_seats(request, movie_id, showtime_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)

    return render(request, "movies/select_seats.html", {
        "movie": movie,
        "showtime": showtime
    })

#Get Seat Availability
def get_seats(request, movie_id, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = Seat.objects.filter(showtime=showtime).order_by('row', 'number')

    seat_data = [
        {
            "id": seat.id,
            "row": seat.row,
            "number": seat.number,
            "seat_class": seat.seat_class,
            "price": seat.price,
            "is_booked": seat.is_booked
        }
        for seat in seats
    ]

    return JsonResponse({"seats": seat_data})

def get_showtimes(request):
    """ Fetch available showtimes for a movie based on date and venue """
    movie_id = request.GET.get("movie_id")
    date_str = request.GET.get("date")
    venue_id = request.GET.get("venue_id")

    if not movie_id or not date_str or not venue_id:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        movie = get_object_or_404(Movie, id=movie_id)
        venue = get_object_or_404(Venue, id=venue_id)

        showtimes = Showtime.objects.filter(
            screen__venue=venue,
            movie=movie,
            datetime__date=selected_date
        ).order_by("datetime")

        return JsonResponse([
            {"id": s.id, "time": s.datetime.strftime("%I:%M %p")}
            for s in showtimes
        ], safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def book_tickets(request, movie_id, showtime_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    context = {
        "movie": movie,
        "showtime": showtime,
    }
    return render(request, "movies/book_tickets.html", context)


