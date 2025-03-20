from django.urls import path
from .views import event_list, event_detail, book_event, event_detail_api,book_event
from apps.payments.views import create_checkout_session
from django.conf.urls.static import static
from django.conf import settings  # ✅ Fix: Import settings



urlpatterns = [
    path('', event_list, name='events_list'),  # Events list page
    path('<int:event_id>/', event_detail, name='event_detail'),  # Event detail page
    path('<int:event_id>/book/', book_event, name='book_event'),  # Booking page
    path('api/events/<int:event_id>/', event_detail_api, name='event-detail-api'),  # API for event details
    path('<int:event_id>/book/', book_event, name='book_event'),
    path('<int:event_id>/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)