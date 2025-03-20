from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.movies.models import Movie, Venue, Screen, Showtime, Seat

class Command(BaseCommand):
    help = "Populate Venues, Screens, Movies, Showtimes, and Seats"

    def handle(self, *args, **kwargs):
        self.create_venues()
        self.create_screens()
        #self.create_movies()
        self.create_showtimes_and_seats()

    def create_venues(self):
        venues = [
            {"name": "IMAX Glasgow", "location": "Glasgow Science Centre", "capacity": 300},
            {"name": "Cineworld Glasgow", "location": "Renfrew Street, Glasgow", "capacity": 450},
            {"name": "Vue Cinemas", "location": "St. Enoch Centre, Glasgow", "capacity": 250}
        ]

        for venue_data in venues:
            venue, created = Venue.objects.get_or_create(**venue_data)
            self.stdout.write(self.style.SUCCESS(f"✅ Venue {'Created' if created else 'Exists'}: {venue.name}"))

    def create_screens(self):
        venues = Venue.objects.all()
        for venue in venues:
            for screen_number in range(1, 4):  # 3 screens per venue
                screen, created = Screen.objects.get_or_create(
                    venue=venue, screen_number=screen_number
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Screen {screen_number} in {venue.name}"))

    def create_movies(self):
        movies_data = [
            {"title": "Inception", "description": "A mind-bending thriller by Christopher Nolan.", "runtime": 148, "genre": "Sci-Fi", "rating": "PG-13", "release_date": "2010-07-16", "poster": "movie_posters/inception.jpg"},
            {"title": "Interstellar", "description": "A journey through space and time.", "runtime": 169, "genre": "Sci-Fi", "rating": "PG-13", "release_date": "2014-11-07", "poster": "movie_posters/interstellar.jpg"},
            {"title": "The Godfather", "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "runtime": 175, "genre": "Crime", "rating": "R", "release_date": "1972-03-24", "poster": "movie_posters/godfather.jpg"},
            {"title": "Captain America: Brave New World", "description": "Sam Wilson takes on the mantle of Captain America.", "runtime": 150, "genre": "Action", "rating": "PG-13", "release_date": "2025-07-26", "poster": "movie_posters/captain_america.jpg"},
            {"title": "Snow White", "description": "A reimagined live-action adaptation of Disney's classic Snow White.", "runtime": 135, "genre": "Fantasy", "rating": "PG", "release_date": "2025-03-21", "poster": "movie_posters/snow_white.jpg"}
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(**movie_data)
            self.stdout.write(self.style.SUCCESS(f"🎬 Movie {'Created' if created else 'Exists'}: {movie.title}"))

    def create_showtimes_and_seats(self):
        movies = Movie.objects.all()
        screens = Screen.objects.all()

        if not movies.exists() or not screens.exists():
            self.stdout.write(self.style.ERROR("⚠️ No movies or screens found! Populate them first."))
            return

        start_date = datetime(timezone.now().year, 4, 1)  # April 1st
        end_date = datetime(timezone.now().year, 4, 20)  # April 30th
        showtimes_per_day = ["12:00 PM", "6:00 PM", "9:00 PM"]

        for movie in movies:
            for screen in screens:
                current_date = start_date
                while current_date <= end_date:
                    for showtime_str in showtimes_per_day:
                        showtime_dt = timezone.make_aware(datetime.strptime(f"{current_date.date()} {showtime_str}", "%Y-%m-%d %I:%M %p"))
                        showtime, created = Showtime.objects.get_or_create(movie=movie, screen=screen, datetime=showtime_dt)

                        # ✅ Optimize Seat Creation
                        self.create_seats(showtime)

                    current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("🎭 Showtimes & Seats populated successfully!"))

    def create_seats(self, showtime):
        seats = []
        seat_rows = ['A', 'B', 'C', 'D', 'E',]
        seats_per_row = 5

        for row in seat_rows:
            for num in range(1, seats_per_row + 1):
                seat_class = 'Gold' if row in ['A', 'B',] else 'Diamond'
                price = 15 if seat_class == 'Gold' else 20

                seats.append(Seat(showtime=showtime, row=row, number=num, seat_class=seat_class, price=price, is_booked=False))

        Seat.objects.bulk_create(seats)
        self.stdout.write(self.style.SUCCESS(f"🎟️ Seats populated for {showtime}"))
