from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.movies.models import Movie, Screen, Showtime

class Command(BaseCommand):
    help = "Populate showtimes for all movies"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        screens = Screen.objects.all()

        if not movies.exists() or not screens.exists():
            self.stdout.write(self.style.ERROR("⚠️ No movies or screens found! Populate them first."))
            return

        # ✅ Define showtimes (April & May)
        start_date = datetime(timezone.now().year, 4, 1)
        end_date = datetime(timezone.now().year, 5, 31)
        showtimes_per_day = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]

        for movie in movies:
            for screen in screens:
                current_date = start_date
                while current_date <= end_date:
                    for showtime_str in showtimes_per_day:
                        showtime_dt = timezone.make_aware(datetime.strptime(f"{current_date.date()} {showtime_str}", "%Y-%m-%d %I:%M %p"))
                        showtime, created = Showtime.objects.get_or_create(movie=movie, screen=screen, datetime=showtime_dt)

                    current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("🎬 Showtimes populated successfully!"))
