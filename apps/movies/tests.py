from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.movies.models import Movie, Venue, Screen, Showtime


class MovieModelTests(TestCase):
    def setUp(self):
        self.poster_file = SimpleUploadedFile("poster.jpg", b"file_content", content_type="image/jpeg")

        self.movie = Movie.objects.create(
            title="Interstellar",
            description="A sci-fi movie",
            runtime=169,
            genre="Sci-Fi",
            rating="PG-13",
            poster=self.poster_file
        )
        self.venue = Venue.objects.create(
            name="IMAX",
            location="City Center",
            capacity=200
        )
        self.screen = Screen.objects.create(
            venue=self.venue,
            screen_number=1
        )
        showtime_date = timezone.now().date() + timedelta(days=1)
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            screen=self.screen,
            datetime=timezone.make_aware(datetime.combine(showtime_date, datetime.min.time()))
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Interstellar")

    def test_venue_str(self):
        self.assertEqual(str(self.venue), "IMAX (City Center)")

    def test_screen_str(self):
        self.assertEqual(str(self.screen), "IMAX - Screen 1")

    def test_showtime_str_format(self):
        expected = f"{self.movie.title} - {self.venue.name} (Screen {self.screen.screen_number}) at {self.showtime.datetime.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.showtime), expected)


class MovieViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.poster_file = SimpleUploadedFile("poster.jpg", b"file_content", content_type="image/jpeg")

        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller",
            runtime=148,
            genre="Sci-Fi",
            rating="PG-13",
            poster=self.poster_file
        )
        self.venue = Venue.objects.create(
            name="Cineplex",
            location="Downtown",
            capacity=100
        )
        self.screen = Screen.objects.create(
            venue=self.venue,
            screen_number=1
        )
        showtime_date = timezone.now().date() + timedelta(days=1)
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            screen=self.screen,
            datetime=timezone.make_aware(datetime.combine(showtime_date, datetime.min.time()))
        )

    def test_movie_list_view(self):
        url = reverse("movie_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_movie_detail_view(self):
        url = reverse("movie_detail", args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertIn("venues", response.context)
        self.assertIn("today", response.context)

    def test_get_showtimes_api(self):
        url = reverse("get_showtimes")
        showtime_date = self.showtime.datetime.date().strftime('%Y-%m-%d')
        response = self.client.get(url, {
            "movie_id": self.movie.id,
            "date": showtime_date,
            "venue_id": self.venue.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertIn("time", response.json()[0])
