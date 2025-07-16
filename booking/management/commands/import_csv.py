import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from booking.models import FitnessClass, Booking
from django.utils import timezone
import pytz

class Command(BaseCommand):
    help = "Import FitnessClass and Booking data from CSV files"

    def add_arguments(self, parser):
        parser.add_argument('--fitness', type=str, help='Path to fitness_classes.csv')
        parser.add_argument('--booking', type=str, help='Path to bookings.csv')

    def handle(self, *args, **options):
        fitness_csv = options['fitness']
        booking_csv = options['booking']

        if fitness_csv:
            self.import_fitness_classes(fitness_csv)
        if booking_csv:
            self.import_bookings(booking_csv)

    def import_fitness_classes(self, filepath):
       
        
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obj, created = FitnessClass.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                      'date_time': timezone.make_aware(parse_datetime(row['date_time']), timezone=pytz.timezone('Asia/Kolkata')),
                        'instructor': row['instructor'],
                        'capacity': int(row['capacity']),
                        'available_slots': int(row['available_slots']),
                    }
                )
                action = "Created" if created else "Skipped"
                self.stdout.write(f"{action} FitnessClass ID {obj.id}")

    def import_bookings(self, filepath):
        
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    fitness_class = FitnessClass.objects.get(id=row['fitness_class'])
                    obj, created = Booking.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'fitness_class': fitness_class,
                            'client_name': row['client_name'],
                            'client_email': row['client_email'],
                            'booking_date': timezone.make_aware(parse_datetime(row['booking_date']), timezone=pytz.timezone('Asia/Kolkata')),
                        }
                    )
                    action = "Created" if created else "Skipped"
                    self.stdout.write(f"{action} Booking ID {obj.id}")
                except FitnessClass.DoesNotExist:
                    self.stderr.write(f"FitnessClass with ID {row['fitness_class']} not found. Skipping booking ID {row['id']}")
