from django.db import models
from django.utils.timezone import now  # Import `now` for DateTime fields
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
    schedule = models.TextField(default="Schedule to be announced.")  # Event timing details
    capacity = models.PositiveIntegerField(default=100)  # Max people allowed

    # New fields replacing old ones
    countdown_start = models.DateTimeField(default=now)  # Countdown Timer Start
    google_maps_embed = models.TextField(blank=True, null=True)  # Google Maps Embed Link
    social_media_links = models.JSONField(default=dict, blank=True, null=True)  # Social media share links
    reviews_enabled = models.BooleanField(default=True)  # Enable/Disable reviews
    ticket_types = models.JSONField(default=dict, blank=True, null=True)  # Stores ticket categories (General, VIP)

    def __str__(self):
        return f"Details for {self.event.title}"
    
class Speaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="speakers")
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='speakers/', blank=True, null=True)

    def __str__(self):
        return self.name

class EventAgenda(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="agenda")
    time_slot = models.TimeField()
    activity = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.time_slot} - {self.activity}"

class Sponsor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sponsors")
    name = models.CharField(max_length=255)
    sponsorship_level = models.CharField(max_length=50, choices=[
        ("Gold", "Gold"),
        ("Silver", "Silver"),
        ("Bronze", "Bronze")
    ])

    def __str__(self):
        return self.name