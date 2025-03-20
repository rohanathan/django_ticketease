from django.core.management.base import BaseCommand
from apps.movies.models import Venue, Screen

class Command(BaseCommand):
    help = "Populate venues and screens"

    def handle(self, *args, **kwargs):
        venues_data = [
            {"name": "IMAX Glasgow", "location": "Glasgow Science Centre", "capacity": 300},
            {"name": "Cineworld Glasgow", "location": "Renfrew Street, Glasgow", "capacity": 450},
            {"name": "Vue Cinemas", "location": "St. Enoch Centre, Glasgow", "capacity": 250},
            {"name": "Odeon Luxe", "location": "Springfield Quay, Glasgow", "capacity": 200},
        ]

        for venue_data in venues_data:
            venue, created = Venue.objects.get_or_create(**venue_data)
            self.stdout.write(self.style.SUCCESS(f"✅ Venue {'Created' if created else 'Exists'}: {venue.name}"))

            # ✅ Add 3 Screens per venue
            for screen_number in range(1, 4):
                screen, created = Screen.objects.get_or_create(venue=venue, screen_number=screen_number)
                self.stdout.write(self.style.SUCCESS(f"🎥 Screen {screen_number} added to {venue.name}"))
