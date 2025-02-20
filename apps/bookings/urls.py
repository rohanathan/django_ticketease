from django.urls import path
from .views import confirm_booking, booking_success

urlpatterns = [
    path("<int:movie_id>/showtime/<int:showtime_id>/confirm-booking/", confirm_booking, name="confirm_booking"),
    path("<int:movie_id>/showtime/<int:showtime_id>/booking-success/", booking_success, name="booking_success"),
]
