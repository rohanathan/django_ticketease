from django.urls import path
from .views import movie_list, movie_detail, select_seats, get_dynamic_showtimes, get_seats, book_tickets

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('<int:movie_id>/', movie_detail, name='movie_detail'),
    path('<int:movie_id>/showtime/<str:showtime_id>/select-seats/', select_seats, name='select_seats'),  # ✅ Fix: Allow showtime_id as string
    path('<int:movie_id>/showtime/<str:showtime_id>/get-seats/', get_seats, name='get_seats'),
    path("api/dynamic-showtimes/", get_dynamic_showtimes, name="get_dynamic_showtimes"),
    path('<int:movie_id>/showtime/<str:showtime_id>/book/', book_tickets, name='book_tickets'),
]
