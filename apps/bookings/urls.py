from django.urls import path
from .views import confirm_booking, booking_success, booking_success_event,my_bookings

urlpatterns = [
    path("<int:movie_id>/showtime/<int:showtime_id>/booking-success/", booking_success, name="booking_success"),
    path("booking-success/event/<int:event_id>/", booking_success_event, name="booking_success_event"),
    path("my-bookings/", my_bookings, name="my_bookings"),

]
