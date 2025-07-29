#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, '/srv/storage/prynsver/projects/wingz')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rides_api.settings')
django.setup()

from rides.models import User, Ride, RideEvent

print("=== Database Status ===")
print(f"Users: {User.objects.count()}")
print(f"Rides: {Ride.objects.count()}")
print(f"Events: {RideEvent.objects.count()}")

admin_exists = User.objects.filter(email='admin@wingz.com', role='admin').exists()
print(f"Admin user exists: {admin_exists}")

if admin_exists:
    admin_user = User.objects.get(email='admin@wingz.com')
    print(f"Admin user: {admin_user.first_name} {admin_user.last_name}")

print("\n=== Sample Rides ===")
for ride in Ride.objects.select_related('id_rider', 'id_driver')[:3]:
    print(f"Ride {ride.id_ride}: {ride.status} - {ride.id_rider.email} -> {ride.id_driver.email}")

print("\n=== Recent Events ===")
for event in RideEvent.objects.select_related('id_ride')[:5]:
    print(f"Event {event.id_ride_event}: {event.description} ({event.created_at})")

print("\n=== Setup Complete ===")
print("The Django application is ready!")
print("Admin credentials: admin@wingz.com / admin123")
print("API endpoints available at: http://localhost:8000/api/v1/")
