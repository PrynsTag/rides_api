#!/usr/bin/env python
"""
API Test Script for Wingz Django Assessment

This script demonstrates the key features of the API:
1. Authentication
2. Ride listing with filtering and sorting
3. Performance optimization
"""

import requests
import json
from requests.auth import HTTPBasicAuth


def test_api():
    base_url = "http://localhost:8000/api/v1"
    auth = HTTPBasicAuth('admin@wingz.com', 'admin123')
    
    print("=== Testing Wingz API ===\n")
    
    # Test 1: Basic ride listing
    print("1. Testing basic ride listing:")
    try:
        response = requests.get(f"{base_url}/rides/", auth=auth, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully retrieved {data['count']} rides")
            print(f"✓ Pagination working: {len(data['results'])} rides per page")
            
            # Show first ride details
            if data['results']:
                ride = data['results'][0]
                print(f"✓ Sample ride: {ride['id_ride']} - {ride['status']}")
                print(f"✓ Driver: {ride['id_driver_data']['first_name']} {ride['id_driver_data']['last_name']}")
                print(f"✓ Rider: {ride['id_rider_data']['first_name']} {ride['id_rider_data']['last_name']}")
                print(f"✓ Today's events: {len(ride['todays_ride_events'])} events")
        else:
            print(f"✗ Failed to retrieve rides: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 2: Filtering by status
    print("2. Testing filtering by status:")
    try:
        response = requests.get(f"{base_url}/rides/?status=completed", auth=auth, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Completed rides: {data['count']}")
        else:
            print(f"✗ Failed to filter rides: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 3: Filtering by rider email
    print("3. Testing filtering by rider email:")
    try:
        response = requests.get(f"{base_url}/rides/?rider_email=john", auth=auth, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Rides with 'john' in rider email: {data['count']}")
        else:
            print(f"✗ Failed to filter by email: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 4: Sorting by pickup time
    print("4. Testing sorting by pickup time:")
    try:
        response = requests.get(f"{base_url}/rides/?ordering=pickup_time", auth=auth, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Rides sorted by pickup time (ascending): {len(data['results'])} rides")
            if len(data['results']) >= 2:
                print(f"✓ First ride pickup: {data['results'][0]['pickup_time']}")
                print(f"✓ Second ride pickup: {data['results'][1]['pickup_time']}")
        else:
            print(f"✗ Failed to sort rides: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 5: Distance-based sorting
    print("5. Testing distance-based sorting:")
    # San Francisco coordinates
    lat, lon = 37.7749, -122.4194
    try:
        response = requests.get(
            f"{base_url}/rides/?lat={lat}&lon={lon}&sort_by_distance=true", 
            auth=auth, 
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Rides sorted by distance from SF: {len(data['results'])} rides")
            if data['results']:
                ride = data['results'][0]
                print(f"✓ Closest ride: {ride['id_ride']} at ({ride['pickup_latitude']}, {ride['pickup_longitude']})")
        else:
            print(f"✗ Failed to sort by distance: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 6: User management
    print("6. Testing user management:")
    try:
        response = requests.get(f"{base_url}/users/", auth=auth, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully retrieved {len(data)} users")
            admin_users = [u for u in data if u['role'] == 'admin']
            drivers = [u for u in data if u['role'] == 'driver']
            riders = [u for u in data if u['role'] == 'rider']
            print(f"✓ Admin users: {len(admin_users)}")
            print(f"✓ Drivers: {len(drivers)}")
            print(f"✓ Riders: {len(riders)}")
        else:
            print(f"✗ Failed to retrieve users: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "="*50)
    print("API Testing Complete!")
    print("="*50)


if __name__ == "__main__":
    print("Make sure the Django server is running:")
    print("python manage.py runserver")
    print("\nThen run this script to test the API.\n")
    
    try:
        test_api()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
