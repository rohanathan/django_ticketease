from django.urls import path
from .views import event_list, event_detail, book_event, event_detail_api
from apps.payments.views import create_checkout_session

urlpatterns = [
    path('', event_list, name='events_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('<int:event_id>/book/', book_event, name='book_event'),
    path('<int:event_id>/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('api/events/<int:event_id>/', event_detail_api, name='event-detail-api'),
    
]
