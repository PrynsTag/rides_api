from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from rides.models import User, Ride, RideEvent


class Command(BaseCommand):
    help = 'Create sample data for testing the API'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@wingz.com',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user')
        
        # Create drivers
        drivers = []
        driver_data = [
            ('Chris', 'H', 'chris.h@wingz.com'),
            ('Howard', 'Y', 'howard.y@wingz.com'),
            ('Randy', 'W', 'randy.w@wingz.com'),
        ]
        
        for first, last, email in driver_data:
            driver, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first,
                    'last_name': last,
                    'role': 'driver',
                    'phone_number': f'+1-555-{random.randint(1000, 9999)}',
                }
            )
            if created:
                driver.set_password('driver123')
                driver.save()
            drivers.append(driver)
        
        # Create riders
        riders = []
        rider_data = [
            ('John', 'Doe', 'john.doe@example.com'),
            ('Jane', 'Smith', 'jane.smith@example.com'),
            ('Bob', 'Johnson', 'bob.johnson@example.com'),
            ('Alice', 'Williams', 'alice.williams@example.com'),
            ('Charlie', 'Brown', 'charlie.brown@example.com'),
        ]
        
        for first, last, email in rider_data:
            rider, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first,
                    'last_name': last,
                    'role': 'rider',
                    'phone_number': f'+1-555-{random.randint(1000, 9999)}',
                }
            )
            if created:
                rider.set_password('rider123')
                rider.save()
            riders.append(rider)
        
        # Create sample rides
        statuses = ['en-route', 'pickup', 'dropoff', 'completed']
        
        # San Francisco Bay Area coordinates for realistic data
        pickup_locations = [
            (37.7749, -122.4194),  # San Francisco
            (37.4419, -122.1430),  # Palo Alto
            (37.6879, -122.4702),  # San Mateo
            (37.5407, -122.2959),  # Redwood City
            (37.3861, -122.0839),  # Mountain View
        ]
        
        dropoff_locations = [
            (37.7849, -122.4094),  # SF Downtown
            (37.4519, -122.1330),  # Stanford
            (37.6979, -122.4802),  # San Mateo Downtown
            (37.5507, -122.2859),  # Redwood City Downtown
            (37.3961, -122.0739),  # Mountain View Downtown
        ]
        
        for i in range(50):
            pickup_lat, pickup_lon = random.choice(pickup_locations)
            dropoff_lat, dropoff_lon = random.choice(dropoff_locations)
            
            # Add some random variation to coordinates
            pickup_lat += random.uniform(-0.01, 0.01)
            pickup_lon += random.uniform(-0.01, 0.01)
            dropoff_lat += random.uniform(-0.01, 0.01)
            dropoff_lon += random.uniform(-0.01, 0.01)
            
            # Random pickup time in the last 30 days
            pickup_time = timezone.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            ride = Ride.objects.create(
                status=random.choice(statuses),
                id_rider=random.choice(riders),
                id_driver=random.choice(drivers),
                pickup_latitude=pickup_lat,
                pickup_longitude=pickup_lon,
                dropoff_latitude=dropoff_lat,
                dropoff_longitude=dropoff_lon,
                pickup_time=pickup_time,
            )
            
            # Create some ride events
            event_descriptions = [
                'Ride requested',
                'Driver assigned',
                'Driver en route to pickup',
                'Status changed to pickup',
                'Passenger picked up',
                'Status changed to dropoff',
                'Passenger dropped off',
                'Ride completed',
            ]
            
            # Create 3-8 events per ride
            num_events = random.randint(3, 8)
            for j in range(num_events):
                event_time = pickup_time + timedelta(minutes=j * random.randint(2, 15))
                
                # Make sure event_time is not in the future
                if event_time > timezone.now():
                    event_time = timezone.now() - timedelta(minutes=random.randint(1, 60))
                
                RideEvent.objects.create(
                    id_ride=ride,
                    description=event_descriptions[min(j, len(event_descriptions) - 1)],
                    created_at=event_time,
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {User.objects.count()} users\n'
                f'- {Ride.objects.count()} rides\n'
                f'- {RideEvent.objects.count()} ride events\n'
                f'\nAdmin credentials: admin@wingz.com / admin123'
            )
        )
