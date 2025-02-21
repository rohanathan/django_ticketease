from django.urls import path
from .views import event_list, event_detail, book_event, event_detail_api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', event_list, name='events_list'),  # Events list page
    path('<int:event_id>/', event_detail, name='event_detail'),  # Event detail page
    path('<int:event_id>/book/', book_event, name='book_event'),  # Booking page
    path('api/events/<int:event_id>/', event_detail_api, name='event-detail-api'),  # API for event details
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)