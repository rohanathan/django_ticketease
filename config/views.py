from django.shortcuts import render
from apps.movies.models import Movie  
from apps.events.models import Event  # Import Event model

def home(request):
    featured_movies = Movie.objects.order_by('-release_date')[:4]  # Fetch latest 4 movies
    featured_events = Event.objects.order_by('-date')[:4]  # Fetch latest 4 events

   

    return render(request, 'home.html', {
        'featured_movies': featured_movies,
        'featured_events': featured_events
    })

def contact_us(request):
    return render(request, "contact_us.html")

def faq(request):
    return render(request, "faq.html")