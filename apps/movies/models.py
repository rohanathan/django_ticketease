from django.db import models

# Movie Model
class Movie(models.Model):
    MOVIE_RATINGS = [
        ("G", "General Audience"),
        ("PG", "Parental Guidance"),
        ("PG-13", "Parents Strongly Cautioned"),
        ("R", "Restricted"),
        ("NC-17", "Adults Only"),
        ("UA", "Universal Adult"),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    runtime = models.PositiveIntegerField(null=True, blank=True, help_text="Runtime in minutes")
    genre = models.CharField(max_length=100, default="Unknown")
    rating = models.CharField(max_length=5, choices=MOVIE_RATINGS, default="G")
    release_date = models.DateField(null=True, blank=True)
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)

    def __str__(self):
        return self.title

# Venue Model
class Venue(models.Model):
    name = models.CharField(max_length=255, verbose_name="Venue Name")
    location = models.CharField(max_length=500, verbose_name="Location")
    capacity = models.PositiveIntegerField(default=100, verbose_name="Capacity")

    class Meta:
        verbose_name = "Venue"
        verbose_name_plural = "Venues"

    def __str__(self):
        return f"{self.name} ({self.location})"

# Screen Model (Each Venue has Multiple Screens)
class Screen(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="screens")
    screen_number = models.PositiveIntegerField(verbose_name="Screen Number")

    class Meta:
        unique_together = ("venue", "screen_number")  # Ensures unique screen numbers per venue
        verbose_name = "Screen"
        verbose_name_plural = "Screens"

    def __str__(self):
        return f"{self.venue.name} - Screen {self.screen_number}"

# Showtime Model (Movie + Screen + Venue + Time)
class Showtime(models.Model):
    movie = models.ForeignKey(
        'movies.Movie',
        on_delete=models.CASCADE,
        related_name='showtimes'
    )
    screen = models.ForeignKey(
        Screen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='showtimes',
        verbose_name="Screen"
    )
    datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Showtime Date & Time"
    )

    class Meta:
        verbose_name = "Showtime"
        verbose_name_plural = "Showtimes"
        ordering = ["datetime"]

    def __str__(self):
        venue_name = self.screen.venue.name if self.screen else "TBA"
        screen_number = self.screen.screen_number if self.screen else "TBA"
        datetime_str = self.datetime.strftime('%Y-%m-%d %H:%M') if self.datetime else "TBA"
        return f"{self.movie.title} - {venue_name} (Screen {screen_number}) at {datetime_str}"

class Seat(models.Model):
    CLASS_CHOICES = [
        ('Diamond', 'Diamond Class'),
        ('Gold', 'Gold Class'),
    ]
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=1)  # A, B, C, etc.
    number = models.IntegerField()  # 1, 2, 3...
    seat_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Ticket price
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.row}{self.number} - {self.seat_class} ({self.price})"