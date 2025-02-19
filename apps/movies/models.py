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
    # Best Practice
    runtime = models.PositiveIntegerField(null=True, blank=True, help_text="Runtime in minutes")
    # Fixed Error 
    genre = models.CharField(max_length=100, default="Unknown")
    # Best Practice  
    rating = models.CharField(max_length=5, choices=MOVIE_RATINGS, default="G")  
    # Best Practice
    release_date = models.DateField(null=True, blank=True)  
    # Allow optional
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)  

    def __str__(self):
        return self.title

#Venue Model
class Venue(models.Model):
    name = models.CharField(max_length=255, verbose_name="Venue Name")
    location = models.CharField(max_length=500, verbose_name="Location")
    capacity = models.PositiveIntegerField(default=100, verbose_name="Capacity")

    class Meta:
        verbose_name = "Venue"
        verbose_name_plural = "Venues"

    def __str__(self):
        return f"{self.name} ({self.location})"
    
#Showtime Model
class Showtime(models.Model):
    movie = models.ForeignKey(
        'movies.Movie',
        on_delete=models.CASCADE,
        related_name='showtimes'
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,  # Allows venue to be NULL
        null=True,
        blank=True,
        verbose_name="Venue"
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
        venue_name = self.venue.name if self.venue else "TBA"
        datetime_str = self.datetime.strftime('%Y-%m-%d %H:%M') if self.datetime else "TBA"
        return f"{self.movie.title} at {venue_name} on {datetime_str}"



from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Screen(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="screens")
    screen_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.venue.name} - Screen {self.screen_number}"

class Showtime(models.Model):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='showtimes')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='showtimes')
    datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.screen.venue.name} (Screen {self.screen.screen_number}) at {self.datetime.strftime('%Y-%m-%d %H:%M')}"
