from django.core.management.base import BaseCommand
from apps.movies.models import Showtime, Seat

class Command(BaseCommand):
    help = 'Populate seats for all available showtimes'

    def handle(self, *args, **kwargs):
        showtime = Showtime.objects.first()
        if not showtime:
            self.stdout.write(self.style.ERROR("No showtime found! Add a showtime first."))
            return

        Seat.objects.filter(showtime=showtime).delete()  # Clear existing seats before populating

        seat_count = 0
        seat_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']  # Now 10 rows
        seats_per_row = 12  # Increase seats per row from 10 to 12

        for row in seat_rows:
            for num in range(1, seats_per_row + 1):  
                seat_class = 'Gold' if row in ['A', 'B', 'C', 'D'] else 'Diamond'
                price = 150 if seat_class == 'Gold' else 200

                Seat.objects.create(
                    showtime=showtime,
                    row=row,
                    number=num,
                    seat_class=seat_class,
                    price=price,
                    is_booked=False
                )
                seat_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully added {seat_count} seats!"))
