from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.movies.models import Movie, Venue, Screen, Showtime
from apps.bookings.models import Booking
from django.contrib.auth import get_user_model

User = get_user_model()

class BookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.client.login(username="testuser", password="pass1234")

        # Dummy poster file to avoid ImageField errors
        self.poster_file = SimpleUploadedFile(
            name="poster.jpg",
            content=b"dummy_image",
            content_type="image/jpeg"
        )

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

        self.showtime = Showtime.objects.create(
            movie=self.movie,
            screen=self.screen,
            datetime=timezone.now() + timedelta(days=1)
        )

        self.booking = Booking.objects.create(
            user=self.user,
            movie=self.movie,
            showtime=self.showtime,
            seat_count=2,
            total_price=30.00,
            category="movie",
            status="confirmed"
        )

    def test_booking_success_view(self):
        url = reverse("booking_success", args=[self.movie.id, self.showtime.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_my_bookings_view(self):
        url = reverse("my_bookings")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_cancel_booking_view(self):
        url = reverse("cancel_booking", args=[self.booking.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("my_bookings"))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "cancelled")

    def test_qr_code_generation(self):
        url = reverse("booking_success", args=[self.movie.id, self.showtime.id])
        response = self.client.get(url)
        self.assertContains(response, "data:image/png;base64")
