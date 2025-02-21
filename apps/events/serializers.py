from rest_framework import serializers
from .models import Event, EventDetail, Speaker, EventAgenda, Sponsor

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name', 'role', 'bio', 'image']

class EventAgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAgenda
        fields = ['time_slot', 'activity']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['name', 'sponsorship_level']

class EventDetailSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateField(source='event.date', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    event_category = serializers.CharField(source='event.category', read_only=True)
    event_price = serializers.DecimalField(source='event.price', max_digits=10, decimal_places=2, read_only=True)
    event_image = serializers.ImageField(source='event.image', read_only=True)

    # Related Data
    speakers = SpeakerSerializer(many=True, read_only=True, source='event.speakers')
    agenda = EventAgendaSerializer(many=True, read_only=True, source='event.agenda')
    sponsors = SponsorSerializer(many=True, read_only=True, source='event.sponsors')

    # Additional Fields
    social_media_links = serializers.JSONField()
    ticket_types = serializers.JSONField()
    reviews_enabled = serializers.BooleanField()

    class Meta:
        model = EventDetail
        fields = [
            'event_title', 'event_date', 'event_location', 'event_category', 'event_price', 'event_image',
            'description', 'schedule', 'capacity', 'social_media_links', 'ticket_types', 'reviews_enabled',
            'speakers', 'agenda', 'sponsors'
        ]
