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

