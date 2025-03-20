from django.core.management.base import BaseCommand
from datetime import time
from django.utils.timezone import now
from apps.events.models import Event, EventDetail, Speaker, EventAgenda, Sponsor


class Command(BaseCommand):
    help = "Populate the database with sample events, speakers, agendas, and sponsors."

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Starting event population...")

        # **1️⃣ Creating Events**
        event_data = [
            {
                "title": "WWE Monday Night Raw",
                "date": "2025-03-24",
                "location": "OVO Hydro, Glasgow",
                "category": "Sports",
                "price": 49.99,
                "image": "event_images/wwe_raw.jpg",
            },
            {
                "title": "Tom Segura: Come Together",
                "date": "2025-03-21",
                "location": "OVO Hydro, Glasgow",
                "category": "Comedy",
                "price": 39.99,
                "image": "event_images/tom_segura.jpg",
            },
            {
                "title": "David Gray - Past and Present Tour",
                "date": "2025-03-22",
                "location": "SEC Armadillo, Glasgow",
                "category": "Music",
                "price": 59.99,
                "image": "event_images/david_gray.jpg",
            },
            {
                "title": "CYD? Regionals Dance Convention",
                "date": "2025-03-23",
                "location": "SEC Centre, Glasgow",
                "category": "Dance",
                "price": 25.00,
                "image": "event_images/cyd_regionals.jpg",
            },
            {
                "title": "Scottish National Whisky Festival",
                "date": "2025-04-05",
                "location": "SEC Glasgow",
                "category": "Festival",
                "price": 19.99,
                "image": "event_images/whisky_festival.jpg",
            },
        ]

        event_instances = []
        for data in event_data:
            event, created = Event.objects.get_or_create(**data)
            if created:
                self.stdout.write(f"✅ Event Created: {event.title}")
            event_instances.append(event)

        # **2️⃣ Creating Event Details**
        event_details = [
            {
                "event": event_instances[0],  # WWE Raw
                "description": "Electrifying wrestling action featuring top WWE stars.",
                "schedule": "7:30 PM - 11:00 PM",
                "capacity": 13000,
                "countdown_start": now(),
                "google_maps_embed": "https://www.google.com/maps/?q=OVO Hydro, Glasgow",
                "social_media_links": {"facebook": "http://facebook.com/wwe"},
                "reviews_enabled": True,
                "ticket_types": {"General": 49.99, "VIP Ringside": 199.99},
            },
            {
                "event": event_instances[1],  # Tom Segura
                "description": "Tom Segura live stand-up comedy special.",
                "schedule": "8:00 PM - 10:00 PM",
                "capacity": 8000,
                "countdown_start": now(),
                "google_maps_embed": "https://www.google.com/maps/?q=OVO Hydro, Glasgow",
                "social_media_links": {"instagram": "http://instagram.com/tomsegura"},
                "reviews_enabled": True,
                "ticket_types": {"Standard": 39.99, "Premium Seats": 89.99},
            },
        ]

        for detail in event_details:
            EventDetail.objects.create(**detail)

        self.stdout.write("✅ Event Details Added!")

        # **3️⃣ Creating Speakers, Agendas & Sponsors**
        speaker_data = [
            {
                "event": event_instances[0],
                "name": "John Cena",
                "role": "WWE Superstar",
                "bio": "Legendary WWE performer.",
                "image": "speakers/john_cena.jpg",
            },
            {
                "event": event_instances[1],
                "name": "Tom Segura",
                "role": "Comedian",
                "bio": "Stand-up comedy legend.",
                "image": "speakers/tom_segura.jpg",
            },
        ]

        agenda_data = [
            {
                "event": event_instances[0],
                "time_slot": time(19, 30),
                "activity": "Opening Matches",
            },
            {
                "event": event_instances[0],
                "time_slot": time(21, 0),
                "activity": "Main Event: Championship Match",
            },
            {
                "event": event_instances[1],
                "time_slot": time(20, 0),
                "activity": "Opening Act",
            },
        ]

        sponsor_data = [
            {
                "event": event_instances[0],
                "name": "Monster Energy",
                "sponsorship_level": "Gold",
            },
            {
                "event": event_instances[1],
                "name": "Comedy Central",
                "sponsorship_level": "Silver",
            },
        ]

        for speaker in speaker_data:
            Speaker.objects.create(**speaker)

        for agenda in agenda_data:
            EventAgenda.objects.create(**agenda)

        for sponsor in sponsor_data:
            Sponsor.objects.create(**sponsor)

        self.stdout.write("✅ Speakers, Agendas, and Sponsors added successfully!")

