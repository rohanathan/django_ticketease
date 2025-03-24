from django.urls import path
from .views import (
    movie_list, movie_detail, get_seats, 
    get_showtimes, book_tickets
)
from apps.payments.views import create_checkout_session  #  Import payment view

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('<int:movie_id>/', movie_detail, name='movie_detail'),
    path('<int:movie_id>/showtime/<int:showtime_id>/get-seats/', get_seats, name='get_seats'),
    path("api/showtimes/", get_showtimes, name="get_showtimes"),
    path('<int:movie_id>/showtime/<int:showtime_id>/book/', book_tickets, name='book_tickets'),
    
    #  **Add payment URL**
    path('<int:movie_id>/showtime/<int:showtime_id>/payment/', create_checkout_session, name='create_checkout_session'),
]
