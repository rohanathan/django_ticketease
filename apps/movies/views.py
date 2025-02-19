from django.shortcuts import render, get_object_or_404
from .models import Movie

# List all movies
def movies_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies_list.html', {'movies': movies})

# Movie detail page
def movies_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)  
    return render(request, 'movies_detail.html', {'movie': movie})
