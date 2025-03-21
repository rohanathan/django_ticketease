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
                "trailer_url": "https://www.youtube.com/watch?v=LifqWf0BAOA&ab_channel=WarnerBros.UK%26Ireland",
            },
            {
                "title": "Interstellar",
                "description": "A journey through space and time.",
                "runtime": 169,
                "genre": "Sci-Fi, Drama",
                "rating": "PG-13",
                "release_date": "2014-11-07",
                "poster": "movie_posters/interstellar_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E&ab_channel=WarnerBros.UK%26Ireland",
            },
            {
                "title": "The Godfather",
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "runtime": 175,
                "genre": "Crime, Drama",
                "rating": "R",
                "release_date": "1972-03-24",
                "poster": "movie_posters/godfather_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=UaVTIH8mujA&ab_channel=ParamountPictures",
            },
            {
                "title": "Captain America: Brave New World",
                "description": "Sam Wilson takes on the mantle of Captain America as he faces new global threats.",
                "runtime": 150,
                "genre": "Action, Superhero",
                "rating": "PG-13",
                "release_date": "2025-07-26",
                "poster": "movie_posters/captain_america_brave_new_world_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=1pHDWnXmK7Y&ab_channel=MarvelEntertainment",
            },
            {
                "title": "Snow White",
                "description": "A reimagined live-action adaptation of Disney's classic Snow White tale, set to release in 2025.",
                "runtime": 135,
                "genre": "Fantasy, Adventure",
                "rating": "PG",
                "release_date": "2025-03-21",
                "poster": "movie_posters/snow_white_2025_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=iV46TJKL8cU&ab_channel=Disney",
            },
            {
                "title": "Dog Man",
                "description": "A canine-crime-fighting film adaptation of Dav Pilkey’s bestselling book.",
                "runtime": 89,
                "genre": "Animation, Comedy, Fantasy",
                "rating": "PG",
                "release_date": "2025-02-07",
                "poster": "movie_posters/dog_man_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=QaJbAennB_Q&ab_channel=UniversalPictures",
            },
            {
                "title": "Bridget Jones: Mad About The Boy",
                "description": "Bridget Jones navigates life as a widow and single mom with the help of her family and friends.",
                "runtime": 125,
                "genre": "Comedy, Drama",
                "rating": "15",
                "release_date": "2025-02-13",
                "poster": "movie_posters/bridget_jones_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=AZr9lYz12jw&ab_channel=UniversalPictures",
            },
            {
                "title": "Mickey 17",
                "description": "Mickey Barnes finds himself in the extraordinary circumstance of working for an employer who demands the ultimate commitment: to die, for a living.",
                "runtime": 137,
                "genre": "Comedy, Fantasy, Sci-Fi",
                "rating": "15",
                "release_date": "2025-03-07",
                "poster": "movie_posters/mickey_17_poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=osYpGSz_0i4&ab_channel=WarnerBros.",
            },
            {
                "title": "Hans Zimmer & Friends: Diamond In The Desert",
                "description": "A live performance of Zimmer’s most loved movie soundtracks, with exclusive behind-the-scenes insights.",
                "runtime": 158,
                "genre": "Music",
                "rating": "12A",
                "release_date": "2025-03-19",
                "poster": "movie_posters/hans_zimmer_poster.jpg",
                "trailer_url": "https://www.youtube.com/embed/ZMO2zV14NCI",
            },
            {
                "title": "September 5",
                "description": "A fresh perspective on the live broadcast coverage of the 1972 Munich Olympics hostage crisis.",
                "runtime": 95,
                "genre": "Drama",
                "rating": "15",
                "release_date": "2025-02-05",
                "poster": "movie_posters/september_5_poster.jpg",
                "trailer_url": "https://www.youtube.com/embed/Azud40CQ3IE",
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
                self.stdout.write(self.style.SUCCESS(f"Created movie: {movie.title}"))
            else:
                self.stdout.write(f"Movie already exists: {movie.title}")

        # --- Step 1: Populate Venues ---
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
                self.stdout.write(self.style.SUCCESS(f"🏢 Created venue: {venue.name}"))
            else:
                self.stdout.write(f"Venue already exists: {venue.name}")