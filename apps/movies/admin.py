from django.contrib import admin
from .models import Movie, Venue, Screen, Showtime

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre', 'rating', 'runtime', 'poster')
    search_fields = ('title', 'genre')
    list_filter = ('genre', 'rating', 'release_date')

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name', 'location')

@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ('venue', 'screen_number')
    list_filter = ('venue',)

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'screen', 'datetime')
    list_filter = ('movie', 'screen__venue', 'datetime')

