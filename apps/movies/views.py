from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Movie, Showtime, Seat

# List all movies
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

# Movie detail page
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Get unique venues where this movie is showing
    venues = movie.showtimes.values("screen__venue__id", "screen__venue__name").distinct()

    return render(
        request, 
        "movies/movie_detail.html", 
        {
            "movie": movie,
            "venues": venues,  # ✅ Pass processed venues to template
        }
    )

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
