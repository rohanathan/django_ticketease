from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Movie, Showtime, Seat, Venue, Screen
from datetime import datetime,date,timedelta

# List all movies
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

# Movie detail page
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    venues = Venue.objects.all()  
    today = datetime.today().date()  

    # Generate the next 5 days
    date_range = [today + timedelta(days=i) for i in range(5)]

    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "venues": venues,
        "date_range": date_range,  # Send date list for filtering
    })


def select_seats(request, movie_id, showtime_id):
    """ Seat selection with dynamic showtime and seat generation """

    # ✅ Ensure `showtime_id` is correctly formatted (e.g., "2-3-0")
    if "-" in showtime_id:
        showtime_parts = showtime_id.split("-")
        if len(showtime_parts) != 3:
            return render(request, "404.html")  # Invalid format

        venue_index = int(showtime_parts[0])  # Venue ID
        screen_index = int(showtime_parts[1])  # Screen Number
        show_index = int(showtime_parts[2])  # Showtime Index

        # ✅ Define Fixed Showtimes (Ensuring consistency)
        showtime_list = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
        if show_index >= len(showtime_list):
            return render(request, "404.html")  # Invalid index

        showtime_time = showtime_list[show_index]  # Extracted time

        # ✅ Retrieve or Create Venue
        venues = list(Venue.objects.all())
        if venue_index >= len(venues):
            return render(request, "404.html")  # Invalid venue index

        venue = venues[venue_index]

        # ✅ Retrieve or Create Screen
        screen, created = Screen.objects.get_or_create(
            venue=venue, screen_number=screen_index + 1
        )

        # ✅ Retrieve or Create Showtime for this Venue & Screen
        showtime_datetime = datetime.combine(datetime.today(), datetime.strptime(showtime_time, "%I:%M %p").time())
        showtime, created = Showtime.objects.get_or_create(
            movie_id=movie_id,
            screen=screen,
            datetime=showtime_datetime
        )

    else:
        # 🎟 Standard showtime lookup (for existing static showtimes)
        showtime = get_object_or_404(Showtime, id=showtime_id)
        
    # ✅ Generate Seats Dynamically (if not present)
    if not Seat.objects.filter(showtime=showtime).exists():
        seat_rows = ['E', 'D', 'C', 'B', 'A']  # Top to Bottom (E → A)
        seats_per_row = 6  # 6 Seats per row

        for row in seat_rows:
            for num in range(1, seats_per_row + 1):
                seat_class = 'Diamond' if row in ['A', 'B'] else 'Gold'
                price = 20 if seat_class == 'Diamond' else 15
                
                Seat.objects.create(
                    showtime=showtime,
                    row=row,
                    number=num,
                    seat_class=seat_class,
                    price=price,
                    is_booked=False
                )

    # ✅ Fetch seats & pass them in row-wise order
    seats = Seat.objects.filter(showtime=showtime).order_by('-row', 'number')

    return render(request, "movies/select_seats.html", {
        "movie": get_object_or_404(Movie, id=movie_id),
        "showtime": showtime,
        "seats": seats,
        "screen_number": showtime.screen.screen_number
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

   
#Dynamic Showtimes
def get_dynamic_showtimes(request):
    """ Generate showtimes dynamically based on the selected date """
    movie_id = request.GET.get("movie_id")
    date_str = request.GET.get("date")

    if not movie_id or not date_str:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        movie = get_object_or_404(Movie, id=movie_id)
        
        # 📌 Dynamic Venue & Screen Assignment (Based on Movie ID)
        venues = Venue.objects.all()
        venue_index = (movie.id - 1) % len(venues)  # Cycle venues
        assigned_venue = venues[venue_index]
        
        screen_number = (movie.id % 10) + 1  # Cycle through screen numbers 1-10
        screen_name = f"Screen {screen_number}"

        # 📌 Define Showtimes
        showtimes = [
            {"time": "12:00 PM"},
            {"time": "3:00 PM"},
            {"time": "6:00 PM"},
            {"time": "9:00 PM"}
        ]

        # 📌 Construct Response Dynamically
        showtime_data = [
            {
                "id": f"{movie.id}-{screen_number}-{idx}",
                "venue": assigned_venue.name,
                "screen": screen_name,
                "time": st["time"],
            }
            for idx, st in enumerate(showtimes)
        ]

        return JsonResponse(showtime_data, safe=False)

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


