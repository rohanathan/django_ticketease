from django.shortcuts import render
from apps.movies.models import Movie  # Import Movie model

def home(request):
    featured_movies = Movie.objects.order_by('-release_date')[:4]  # Show latest 4 movies
    return render(request, 'home.html', {'featured_movies': featured_movies})
