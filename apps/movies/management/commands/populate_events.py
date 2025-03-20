from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import time
from apps.events.models import Event, EventDetail, Speaker, EventAgenda, Sponsor

class Command(BaseCommand):
    help = "Populate the database with sample events, details, speakers, agendas, and sponsors."

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting event population...")

        # --- Create 10 Sample Events ---
        events_data = [
            {
                "title": "WWE Monday Night Raw",
                "date": "2025-03-24",
                "location": "OVO Hydro, Glasgow",
                "category": "Sports",
                "price": 49.99,
                "image": "event_images/wwe_raw.jpg"
            },
            {
                "title": "Tom Segura: Come Together",
                "date": "2025-03-21",
                "location": "OVO Hydro, Glasgow",
                "category": "Comedy",
                "price": 39.99,
                "image": "event_images/tom_segura.jpg"
            },
            {
                "title": "David Gray - Past and Present Tour",
                "date": "2025-03-22",
                "location": "SEC Armadillo, Glasgow",
                "category": "Music",
                "price": 59.99,
                "image": "event_images/david_gray.jpg"
            },
            {
                "title": "CYD? Regionals Dance Convention",
                "date": "2025-03-23",
                "location": "SEC Centre, Glasgow",
                "category": "Dance",
                "price": 25.00,
                "image": "event_images/cyd_regionals.jpg"
            },
            {
                "title": "Scottish National Whisky Festival",
                "date": "2025-04-05",
                "location": "SEC Glasgow",
                "category": "Festival",
                "price": 19.99,
                "image": "event_images/whisky_festival.jpg"
            },
            {
                "title": "The Wombats - Everything Everything",
                "date": "2025-03-25",
                "location": "OVO Hydro, Glasgow",
                "category": "Music",
                "price": 45.00,
                "image": "event_images/wombats.jpg"
            },
            {
                "title": "Wardruna - Nordic Music Experience",
                "date": "2025-03-25",
                "location": "SEC Armadillo, Glasgow",
                "category": "Music",
                "price": 50.00,
                "image": "event_images/wardruna.jpg"
            },
            {
                "title": "Gabrielle - The Hits Live",
                "date": "2025-04-02",
                "location": "SEC Armadillo, Glasgow",
                "category": "Music",
                "price": 34.99,
                "image": "event_images/gabrielle.jpg"
            },
            {
                "title": "Nikita Kuzmin - Midnight Dancer",
                "date": "2025-04-03",
                "location": "SEC Armadillo, Glasgow",
                "category": "Dance",
                "price": 29.99,
                "image": "event_images/nikita_kuzmin.jpg"
            },
            {
                "title": "Jeff Wayne's War of the Worlds",
                "date": "2025-04-02",
                "location": "OVO Hydro, Glasgow",
                "category": "Theatre",
                "price": 79.99,
                "image": "event_images/war_of_the_worlds.jpg"
            }
        ]

        events = {}
        for data in events_data:
            event, created = Event.objects.get_or_create(
                title=data["title"],
                defaults=data
            )
            events[data["title"]] = event
            if created:
                self.stdout.write(f"Created event: {data['title']}")
            else:
                self.stdout.write(f"Event already exists: {data['title']}")

        # --- Create EventDetail for Events 1-5 ---
        details_data = {
            "WWE Monday Night Raw": {
                "description": "Experience electrifying wrestling action featuring your favorite WWE superstars.",
                "schedule": "7:30 PM - 11:00 PM",
                "capacity": 13000,
                "google_maps_embed": "https://www.google.com/maps/?q=OVO Hydro, Glasgow",
                "social_media_links": {"facebook": "http://facebook.com/wwe", "twitter": "http://twitter.com/wwe"},
                "reviews_enabled": True,
                "ticket_types": {"General": 49.99, "VIP Ringside": 199.99}
            },
            "Tom Segura: Come Together": {
                "description": "Tom Segura brings his hilarious stand-up comedy special 'Come Together' live.",
                "schedule": "8:00 PM - 10:00 PM",
                "capacity": 8000,
                "google_maps_embed": "https://www.google.com/maps/?q=OVO Hydro, Glasgow",
                "social_media_links": {"instagram": "http://instagram.com/tomsegura"},
                "reviews_enabled": True,
                "ticket_types": {"Standard": 39.99, "Premium Seats": 89.99}
            },
            "David Gray - Past and Present Tour": {
                "description": "David Gray performs his greatest hits in an unforgettable musical journey.",
                "schedule": "7:00 PM - 10:00 PM",
                "capacity": 3000,
                "google_maps_embed": "https://www.google.com/maps/?q=SEC Armadillo, Glasgow",
                "social_media_links": {"twitter": "http://twitter.com/davidgray"},
                "reviews_enabled": True,
                "ticket_types": {"General Admission": 59.99, "VIP Package": 129.99}
            },
            "CYD? Regionals Dance Convention": {
                "description": "Join the ultimate dance convention and showcase your skills.",
                "schedule": "9:00 AM - 6:00 PM",
                "capacity": 2500,
                "google_maps_embed": "https://www.google.com/maps/?q=SEC Centre, Glasgow",
                "social_media_links": {"facebook": "http://facebook.com/cydregionals"},
                "reviews_enabled": True,
                "ticket_types": {"Participant": 25.00, "Spectator": 15.00}
            },
            "Scottish National Whisky Festival": {
                "description": "Celebrate Scotland's whisky heritage with tastings, masterclasses, and more.",
                "schedule": "12:00 PM - 8:00 PM",
                "capacity": 4000,
                "google_maps_embed": "https://www.google.com/maps/?q=SEC Glasgow",
                "social_media_links": {"instagram": "http://instagram.com/scotwhiskyfest"},
                "reviews_enabled": True,
                "ticket_types": {"General Admission": 19.99, "VIP Whisky Pass": 69.99}
            }
        }

        # --- Create EventDetail for Events 6-10 ---
        details_data_6_10 = {
            "The Wombats - Everything Everything": {
                "description": "The Wombats present 'Everything Everything', a night of indie-rock hits.",
                "schedule": "8:00 PM - 11:00 PM",
                "capacity": 12000,
                "google_maps_embed": "https://www.google.com/maps/?q=OVO Hydro, Glasgow",
                "social_media_links": {"twitter": "http://twitter.com/thewombats"},
                "reviews_enabled": True,
                "ticket_types": {"Regular": 45.00, "VIP Access": 99.99}
            },
            "Wardruna - Nordic Music Experience": {
                "description": "A powerful live Nordic music experience by Wardruna.",
                "schedule": "7:00 PM - 10:00 PM",
                "capacity": 3000,
                "google_maps_embed": "https://www.google.com/maps/?q=SEC Armadillo, Glasgow",
                "social_media_links": {"facebook": "http://facebook.com/wardruna"},
                "reviews_enabled": True,
                "ticket_types": {"Standard Seat": 50.00, "VIP Meet & Greet": 120.00}
            },
            "Gabrielle - The Hits Live": {
                "description": "Gabrielle takes the stage to perform her classic hits live.",
                "schedule": "8:00 PM - 10:00 PM",
                "capacity": 3000,
                "google_maps_embed": "https://www.google.com/maps/?q=SEC Armadillo, Glasgow",
                "social_media_links": {"instagram": "http://instagram.com/gabrielleuk"},
                "reviews_enabled": True,
                "ticket_types": {"General Admission": 34.99, "Front Row": 89.99}
            },
            "Nikita Kuzmin - Midnight Dancer": {
                "description": "An evening of breathtaking dance performances by Nikita Kuzmin.",
                "schedule": "7:30 PM - 10:00 PM",
                "capacity": 2500,
                "google_maps_embed": "https://www.google.com/maps/?q=SEC Armadillo, Glasgow",
                "social_media_links": {"facebook": "http://facebook.com/nikitakuzmin"},
                "reviews_enabled": True,
                "ticket_types": {"Regular Seat": 29.99, "VIP Experience": 79.99}
            },
            "Jeff Wayne's War of the Worlds": {
                "description": "Jeff Wayne's spectacular musical version of 'War of the Worlds' comes to life.",
                "schedule": "7:30 PM - 10:30 PM",
                "capacity": 13500,
                "google_maps_embed": "https://www.google.com/maps/?q=OVO Hydro, Glasgow",
                "social_media_links": {"twitter": "http://twitter.com/jeffwaynewotw"},
                "reviews_enabled": True,
                "ticket_types": {"Standard": 79.99, "Golden Circle": 159.99}
            }
        }


        for title, detail in details_data.items():
            event = events.get(title)
            if event:
                ed, created = EventDetail.objects.get_or_create(
                    event=event,
                    defaults={
                        "description": detail["description"],
                        "schedule": detail["schedule"],
                        "capacity": detail["capacity"],
                        "countdown_start": now(),
                        "google_maps_embed": detail["google_maps_embed"],
                        "social_media_links": detail["social_media_links"],
                        "reviews_enabled": detail["reviews_enabled"],
                        "ticket_types": detail["ticket_types"],
                    }
                )
                if created:
                    self.stdout.write(f"Created EventDetail for: {title}")
                else:
                    self.stdout.write(f"EventDetail already exists for: {title}")

        
        # --- Create EventDetail for Events 6-10 ---
        for title, detail in details_data_6_10.items():
            event = events.get(title)
            if event:
                ed, created = EventDetail.objects.get_or_create(
                    event=event,
                    defaults={
                        "description": detail["description"],
                        "schedule": detail["schedule"],
                        "capacity": detail["capacity"],
                        "countdown_start": now(),
                        "google_maps_embed": detail["google_maps_embed"],
                        "social_media_links": detail["social_media_links"],
                        "reviews_enabled": detail["reviews_enabled"],
                        "ticket_types": detail["ticket_types"],
                    }
                )
                if created:
                    self.stdout.write(f"Created EventDetail for: {title}")
                else:
                    self.stdout.write(f"EventDetail already exists for: {title}")


        # --- Create Speakers, Agendas, and Sponsors for Events 1-5 ---
        # Event 1: WWE Monday Night Raw
        event = events.get("WWE Monday Night Raw")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="John Cena",
                defaults={"role": "WWE Superstar", "bio": "Legendary WWE performer.", "image": "speakers/john_cena.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 30),
                defaults={"activity": "Opening Matches"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(21, 0),
                defaults={"activity": "Main Event: Championship Match"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="Monster Energy",
                defaults={"sponsorship_level": "Gold"}
            )

        # Event 2: Tom Segura: Come Together
        event = events.get("Tom Segura: Come Together")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="Tom Segura",
                defaults={"role": "Comedian", "bio": "Stand-up comedy superstar known for Netflix specials.", "image": "speakers/tom_segura.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 0),
                defaults={"activity": "Opening Act"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 45),
                defaults={"activity": "Main Performance by Tom Segura"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="Comedy Central",
                defaults={"sponsorship_level": "Silver"}
            )

        # Event 3: David Gray - Past and Present Tour
        event = events.get("David Gray - Past and Present Tour")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="David Gray",
                defaults={"role": "Singer-Songwriter", "bio": "Multi-platinum selling artist.", "image": "speakers/david_gray.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 0),
                defaults={"activity": "Doors Open"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 0),
                defaults={"activity": "David Gray Live Performance"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="Spotify",
                defaults={"sponsorship_level": "Gold"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="BBC Radio 2",
                defaults={"sponsorship_level": "Silver"}
            )

        # --- Create Speakers, Agendas, and Sponsors for Events 6-10 ---
        # Event 6: The Wombats - Everything Everything
        event = events.get("The Wombats - Everything Everything")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="Matthew Murphy",
                defaults={"role": "Lead Vocalist", "bio": "Frontman of The Wombats.", "image": "speakers/matthew_murphy.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 0),
                defaults={"activity": "Doors Open"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 0),
                defaults={"activity": "Support Act Performance"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(21, 0),
                defaults={"activity": "Main Performance by The Wombats"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="NME Magazine",
                defaults={"sponsorship_level": "Gold"}
            )

        # Event 7: Wardruna - Nordic Music Experience
        event = events.get("Wardruna - Nordic Music Experience")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="Einar Selvik",
                defaults={"role": "Composer and Vocalist", "bio": "Founder and main composer of Wardruna.", "image": "speakers/einar_selvik.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(18, 30),
                defaults={"activity": "Doors Open"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 30),
                defaults={"activity": "Wardruna Live Performance"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(22, 0),
                defaults={"activity": "Fan Meet & Greet"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="Nordic Spirit",
                defaults={"sponsorship_level": "Silver"}
            )

        # Event 8: Gabrielle - The Hits Live
        event = events.get("Gabrielle - The Hits Live")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="Gabrielle",
                defaults={"role": "Singer", "bio": "Award-winning British singer-songwriter.", "image": "speakers/gabrielle.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 0),
                defaults={"activity": "Doors Open"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 0),
                defaults={"activity": "Opening Act"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 45),
                defaults={"activity": "Gabrielle Live Performance"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="BBC Radio Scotland",
                defaults={"sponsorship_level": "Gold"}
            )

        # Event 9: Nikita Kuzmin - Midnight Dancer
        event = events.get("Nikita Kuzmin - Midnight Dancer")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="Nikita Kuzmin",
                defaults={"role": "Professional Dancer", "bio": "Internationally recognized ballroom and Latin dancer.", "image": "speakers/nikita_kuzmin.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(18, 30),
                defaults={"activity": "Doors Open"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 30),
                defaults={"activity": "Dance Performances"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(21, 0),
                defaults={"activity": "Interactive Dance Workshop"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="DanceSport Scotland",
                defaults={"sponsorship_level": "Silver"}
            )

        # Event 10: Jeff Wayne's War of the Worlds
        event = events.get("Jeff Wayne's War of the Worlds")
        if event:
            Speaker.objects.get_or_create(
                event=event,
                name="Jeff Wayne",
                defaults={"role": "Composer", "bio": "Legendary composer known for the musical version of 'War of the Worlds'.", "image": "speakers/jeff_wayne.jpg"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(19, 0),
                defaults={"activity": "Doors Open"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(20, 0),
                defaults={"activity": "Act I Performance"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(21, 30),
                defaults={"activity": "Intermission"}
            )
            EventAgenda.objects.get_or_create(
                event=event,
                time_slot=time(21, 45),
                defaults={"activity": "Act II Performance"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="Classic FM",
                defaults={"sponsorship_level": "Gold"}
            )
            Sponsor.objects.get_or_create(
                event=event,
                name="Sony Music",
                defaults={"sponsorship_level": "Silver"}
            )

        self.stdout.write(self.style.SUCCESS("✅ Event details, speakers, agendas, and sponsors populated successfully!"))
