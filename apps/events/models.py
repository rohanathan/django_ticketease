from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255, default="Untitled Event")
    date = models.DateField(null=True, blank=True)  # Allows events without a date
    location = models.CharField(max_length=255, default="To be announced")
    category = models.CharField(max_length=100, default="General")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', default='event_images/default.jpg')  # Default image

    def __str__(self):
        return f"{self.title} - {self.date if self.date else 'No Date'}"
class EventDetail(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="details")  # One-to-One relationship
    description = models.TextField(default="No description available.")
    schedule = models.TextField(default="Schedule to be announced.")  # Details about event timing
    speakers = models.TextField(blank=True, null=True)  # List of speakers for conferences
    agenda = models.TextField(blank=True, null=True)  # Detailed agenda or lineup
    sponsors = models.TextField(blank=True, null=True)  # Sponsors of the event
    capacity = models.PositiveIntegerField(default=100)  # Max people allowed

    def __str__(self):
        return f"Details for {self.event.title}"