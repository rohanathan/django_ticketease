from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# events/views.py (or payments/views.py)
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Event

from .models import Event, EventDetail
from .serializers import EventDetailSerializer

# Event List Page
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/events_list.html', {'events': events})

# Booking Page
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/book_event.html', {'event': event})
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/events_detail.html', {'event_id': event.id,'event_location': event.location,'event':event})



# API for Event Details
@api_view(['GET'])
def event_detail_api(request, event_id):
    event_detail = get_object_or_404(EventDetail, event__id=event_id)
    serializer = EventDetailSerializer(event_detail)
    return Response(serializer.data, status=status.HTTP_200_OK)
