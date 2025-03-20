from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.movies.models import Movie, Venue, Screen, Showtime

class Command(BaseCommand):
    help = "Populate sample movies, venues, screens, and showtimes."

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Starting movie population...")

        # --- Create 10 Sample Movies ---
        movies_data = [
            {
                "title": "Inception",
                "description": "A mind-bending thriller by Christopher Nolan.",
                "runtime": 148,
                "genre": "Sci-Fi, Thriller",
                "rating": "PG-13",
                "release_date": "2010-07-16",
                "poster": "movie_posters/inception_poster.jpg",
            },
            {
                "title": "Interstellar",
                "description": "A journey through space and time.",
                "runtime": 169,
                "genre": "Sci-Fi, Drama",
                "rating": "PG-13",
                "release_date": "2014-11-07",
                "poster": "movie_posters/interstellar_poster.jpg",
            },
            {
                "title": "The Godfather",
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "runtime": 175,
                "genre": "Crime, Drama",
                "rating": "R",
                "release_date": "1972-03-24",
                "poster": "movie_posters/godfather_poster.jpg",
            },
            {
                "title": "Captain America: Brave New World",
                "description": "Sam Wilson takes on the mantle of Captain America as he faces new global threats.",
                "runtime": 150,
                "genre": "Action, Superhero",
                "rating": "PG-13",
                "release_date": "2025-07-26",
                "poster": "movie_posters/captain_america_brave_new_world_poster.jpg",
            },
            {
                "title": "Snow White",
                "description": "A reimagined live-action adaptation of Disney's classic Snow White tale, set to release in 2025.",
                "runtime": 135,
                "genre": "Fantasy, Adventure",
                "rating": "PG",
                "release_date": "2025-03-21",
                "poster": "movie_posters/snow_white_2025_poster.jpg",
            },
            {
                "title": "Dog Man",
                "description": "A canine-crime-fighting film adaptation of Dav Pilkey’s bestselling book.",
                "runtime": 89,
                "genre": "Animation, Comedy, Fantasy",
                "rating": "PG",
                "release_date": "2025-02-07",
                "poster": "movie_posters/dog_man_poster.jpg",
            },
            {
                "title": "Bridget Jones: Mad About The Boy",
                "description": "Bridget Jones navigates life as a widow and single mom with the help of her family and friends.",
                "runtime": 125,
                "genre": "Comedy, Drama",
                "rating": "15",
                "release_date": "2025-02-13",
                "poster": "movie_posters/bridget_jones_poster.jpg",
            },
            {
                "title": "Mickey 17",
                "description": "Mickey Barnes finds himself in the extraordinary circumstance of working for an employer who demands the ultimate commitment: to die, for a living.",
                "runtime": 137,
                "genre": "Comedy, Fantasy, Sci-Fi",
                "rating": "15",
                "release_date": "2025-03-07",
                "poster": "movie_posters/mickey_17_poster.jpg",
            },
            {
                "title": "Hans Zimmer & Friends: Diamond In The Desert",
                "description": "A live performance of Zimmer’s most loved movie soundtracks, with exclusive behind-the-scenes insights.",
                "runtime": 158,
                "genre": "Music",
                "rating": "12A",
                "release_date": "2025-03-19",
                "poster": "movie_posters/hans_zimmer_poster.jpg",
            },
            {
                "title": "September 5",
                "description": "A fresh perspective on the live broadcast coverage of the 1972 Munich Olympics hostage crisis.",
                "runtime": 95,
                "genre": "Drama",
                "rating": "15",
                "release_date": "2025-02-05",
                "poster": "movie_posters/september_5_poster.jpg",
            },
        ]

        movies = {}
        for data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=data["title"],
                defaults=data
            )
            movies[data["title"]] = movie
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created movie: {movie.title}"))
            else:
                self.stdout.write(f"Movie already exists: {movie.title}")

        # --- Populate Venues and Screens ---
        venues_data = [
            {"name": "IMAX Glasgow", "location": "Glasgow Science Centre", "capacity": 300},
            {"name": "Cineworld Glasgow", "location": "Renfrew Street, Glasgow", "capacity": 450},
            {"name": "Vue Cinemas", "location": "St. Enoch Centre, Glasgow", "capacity": 250},
            {"name": "Odeon Luxe", "location": "Springfield Quay, Glasgow", "capacity": 200},
        ]

        venues = {}
        for venue_data in venues_data:
            venue, created = Venue.objects.get_or_create(**venue_data)
            venues[venue.name] = venue
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created venue: {venue.name}"))
            else:
                self.stdout.write(f"Venue already exists: {venue.name}")

            # Create 3 screens per venue
            for screen_number in range(1, 4):
                screen, created = Screen.objects.get_or_create(venue=venue, screen_number=screen_number)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"🎥 Created Screen {screen_number} for {venue.name}"))
                else:
                    self.stdout.write(f"Screen {screen_number} already exists for {venue.name}")

        # --- Populate Showtimes for All Movies ---
        # Define the showtime range (for April and May of the current year)
        current_year = timezone.now().year
        start_date = datetime(current_year, 4, 1)
        end_date = datetime(current_year, 5, 31)
        showtimes_per_day = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]

        all_screens = Screen.objects.all()
        if not movies or not all_screens:
            self.stdout.write(self.style.ERROR("⚠️ No movies or screens found!"))
            return

        for movie in Movie.objects.all():
            for screen in all_screens:
                current_date = start_date
                while current_date <= end_date:
                    for showtime_str in showtimes_per_day:
                        dt_str = f"{current_date.date()} {showtime_str}"
                        try:
                            showtime_dt = timezone.make_aware(datetime.strptime(dt_str, "%Y-%m-%d %I:%M %p"))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error parsing date: {dt_str} - {e}"))
                            continue
                        Showtime.objects.get_or_create(movie=movie, screen=screen, datetime=showtime_dt)
                    current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("🎬 Showtimes populated successfully for all movies!"))
