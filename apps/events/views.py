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
    return render(request, 'events/events_detail.html', {'event_id': event.id,'event_location': event.location})



# API for Event Details
@api_view(['GET'])
def event_detail_api(request, event_id):
    event_detail = get_object_or_404(EventDetail, event__id=event_id)
    serializer = EventDetailSerializer(event_detail)
    return Response(serializer.data, status=status.HTTP_200_OK)



def create_event_checkout_session(request, event_id):
    if request.method == "POST":
        total_price = request.POST.get("total_price", "0.00")
        ticket_details = request.POST.get("ticket_details", "{}")
        # Optionally parse the ticket_details JSON if needed

        # Convert total price to cents for Stripe
        amount_in_cents = int(float(total_price) * 100)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create the checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"TicketEase - Event {event_id}",
                    },
                    'unit_amount': amount_in_cents,  # total price in cents
                },
                'quantity': 1,  # 1 "bundle" of tickets
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        )

        return redirect(checkout_session.url, code=303)

    # If not POST, maybe redirect to event booking page
    return redirect('book_event', event_id=event_id)
