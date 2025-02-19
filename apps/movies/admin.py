from django.contrib import admin
from .models import Movie, Showtime

# Register your models here.
#admin.site.register(Movie)
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre', 'rating', 'runtime', 'poster')
    search_fields = ('title', 'genre')
    list_filter = ('genre', 'rating', 'release_date')


admin.site.register(Showtime)