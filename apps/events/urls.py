from django.urls import path
from .views import event_list, event_detail, book_event

urlpatterns = [
    path('', event_list, name='events_list'),
    path('<int:event_id>/', event_detail, name='events_detail'),
    path('<int:event_id>/book/', book_event, name='book_event'),  # Add this line
]
