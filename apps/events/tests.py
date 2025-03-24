from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, time
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.events.models import Event, EventDetail, Speaker, EventAgenda, Sponsor


class EventModelTests(TestCase):
    def setUp(self):
        self.image_file = SimpleUploadedFile("event.jpg", b"file_content", content_type="image/jpeg")
        self.event = Event.objects.create(
            title="Tech Conference",
            date=timezone.now().date() + timedelta(days=10),
            location="Convention Center",
            category="Technology",
            price=99.99,
            image=self.image_file
        )
        self.details = EventDetail.objects.create(
            event=self.event,
            description="Full day tech talks",
            schedule="10:00 AM - 5:00 PM",
            capacity=500,
        )
        self.speaker = Speaker.objects.create(
            event=self.event,
            name="Alice Smith",
            role="Keynote Speaker",
            bio="Tech Enthusiast",
            image=self.image_file
        )
        self.agenda = EventAgenda.objects.create(
            event=self.event,
            time_slot=time(10, 0),
            activity="Opening Keynote"
        )
        self.sponsor = Sponsor.objects.create(
            event=self.event,
            name="TechCorp",
            sponsorship_level="Gold"
        )

    def test_event_str(self):
        self.assertIn("Tech Conference", str(self.event))

    def test_event_detail_str(self):
        self.assertIn("Tech Conference", str(self.details))

    def test_speaker_str(self):
        self.assertEqual(str(self.speaker), "Alice Smith")

    def test_agenda_str(self):
        self.assertEqual(str(self.agenda), "10:00:00 - Opening Keynote")

    def test_sponsor_str(self):
        self.assertEqual(str(self.sponsor), "TechCorp")


class EventViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            title="Music Festival",
            date=timezone.now().date() + timedelta(days=20),
            location="Open Grounds",
            category="Music",
            price=49.99
        )
        self.event_detail = EventDetail.objects.create(
            event=self.event,
            description="Live performances by top artists",
            schedule="2:00 PM - 11:00 PM",
            capacity=1000
        )

    def test_event_list_view(self):
        url = reverse("events_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Music Festival")

    def test_event_detail_view(self):
        url = reverse("event_detail", args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.location)

    def test_event_detail_api(self):
        url = reverse("event-detail-api", args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Live performances by top artists")
