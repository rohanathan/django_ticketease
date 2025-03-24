from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from apps.movies.models import Movie, Venue, Screen, Showtime
from apps.events.models import Event
from datetime import timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class PaymentFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.poster_file = SimpleUploadedFile("poster.jpg", b"file_content", content_type="image/jpeg")
        self.movie = Movie.objects.create(title="Avatar", runtime=120, genre="Action", rating="PG-13", poster=self.poster_file)
        self.venue = Venue.objects.create(name="Cineplex", location="Downtown", capacity=100)
        self.screen = Screen.objects.create(venue=self.venue, screen_number=1)
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            screen=self.screen,
            datetime=timezone.now() + timedelta(days=1)
        )
        self.event = Event.objects.create(title="Tech Conference", price=100)

    @patch("stripe.checkout.Session.create")
    def test_movie_checkout_redirect(self, mock_stripe_create):
        mock_stripe_create.return_value.url = "https://checkout.stripe.com/testsession"
        url = reverse("create_checkout")
        response = self.client.get(url, {
            "movie_id": self.movie.id,
            "showtime_id": self.showtime.id,
            "tickets": 2,
            "price": 150
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("stripe.com", response.url)

    @patch("stripe.checkout.Session.create")
    def test_event_checkout_redirect(self, mock_stripe_create):
        mock_stripe_create.return_value.url = "https://checkout.stripe.com/testsession"
        url = reverse("create_checkout")
        response = self.client.get(url, {
            "event_id": self.event.id,
            "tickets": 1,
            "price": 100
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("stripe.com", response.url)
