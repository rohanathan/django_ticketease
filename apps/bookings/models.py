from django.db import models
from django.conf import settings
from apps.movies.models import Movie, Showtime
from apps.events.models import Event  # import from events app

class Booking(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('event', 'Event'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)  # new field for events
    # For movies, this represents seat count; for events, it can represent ticket count.
    seat_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.OneToOneField("payments.Payment", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="movie")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} on {self.created_at}"
