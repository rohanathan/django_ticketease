from django.urls import path
from .views import movie_list, movie_detail, select_seats, get_seats

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('<int:movie_id>/', movie_detail, name='movie_detail'),
    path('<int:movie_id>/showtime/<int:showtime_id>/select-seats/', select_seats, name='select_seats'),
    path('<int:movie_id>/showtime/<int:showtime_id>/get-seats/', get_seats, name='get_seats'),
]
