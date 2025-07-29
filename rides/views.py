from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Prefetch, F, Q
from django.utils import timezone
from datetime import timedelta
import math

from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideCreateUpdateSerializer, RideEventSerializer
from .filters import RideFilter
from .permissions import IsAdminUser


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using Haversine formula
    Returns distance in kilometers
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers
    r = 6371
    
    return c * r


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ride model with optimized queries and advanced filtering
    """
    permission_classes = [IsAdminUser]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time']
    
    def get_queryset(self):
        """
        Optimized queryset that minimizes database queries
        """
        # Base queryset with select_related for foreign keys
        queryset = Ride.objects.select_related('id_rider', 'id_driver')
        
        # Prefetch only recent ride events (last 24 hours) for performance
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        recent_events_prefetch = Prefetch(
            'ride_events',
            queryset=RideEvent.objects.filter(created_at__gte=twenty_four_hours_ago),
            to_attr='recent_events'
        )
        queryset = queryset.prefetch_related(recent_events_prefetch)
        
        # Handle distance-based sorting if GPS coordinates are provided
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        sort_by_distance = self.request.query_params.get('sort_by_distance')
        
        if lat and lon and sort_by_distance:
            try:
                user_lat = float(lat)
                user_lon = float(lon)
                
                # Add distance calculation and sort
                # Note: For very large datasets, you might want to use raw SQL or 
                # database-specific functions for better performance
                rides_with_distance = []
                for ride in queryset:
                    distance = calculate_distance(
                        user_lat, user_lon, 
                        ride.pickup_latitude, ride.pickup_longitude
                    )
                    rides_with_distance.append((ride, distance))
                
                # Sort by distance
                rides_with_distance.sort(key=lambda x: x[1])
                
                # Extract just the ride objects
                sorted_ride_ids = [ride.id_ride for ride, _ in rides_with_distance]
                
                # Preserve the distance-based order in the queryset
                # This is a bit of a hack but maintains the order
                preserved_order = {id: index for index, id in enumerate(sorted_ride_ids)}
                queryset = queryset.filter(id_ride__in=sorted_ride_ids)
                queryset = sorted(queryset, key=lambda x: preserved_order[x.id_ride])
                
                return queryset
                
            except ValueError:
                pass  # Invalid lat/lon values, ignore distance sorting
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return RideCreateUpdateSerializer
        return RideSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Custom list method to handle distance-based sorting with pagination
        """
        # Check if distance sorting is requested
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        sort_by_distance = request.query_params.get('sort_by_distance')
        
        if lat and lon and sort_by_distance:
            # For distance-based sorting, we need to handle pagination differently
            try:
                user_lat = float(lat)
                user_lon = float(lon)
                
                # Get the base queryset without distance sorting
                queryset = Ride.objects.select_related('id_rider', 'id_driver')
                twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
                recent_events_prefetch = Prefetch(
                    'ride_events',
                    queryset=RideEvent.objects.filter(created_at__gte=twenty_four_hours_ago),
                    to_attr='recent_events'
                )
                queryset = queryset.prefetch_related(recent_events_prefetch)
                
                # Apply filters
                queryset = self.filter_queryset(queryset)
                
                # Calculate distances and sort
                rides_with_distance = []
                for ride in queryset:
                    distance = calculate_distance(
                        user_lat, user_lon, 
                        ride.pickup_latitude, ride.pickup_longitude
                    )
                    rides_with_distance.append((ride, distance))
                
                rides_with_distance.sort(key=lambda x: x[1])
                sorted_rides = [ride for ride, _ in rides_with_distance]
                
                # Manual pagination
                page = self.paginate_queryset(sorted_rides)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                
                serializer = self.get_serializer(sorted_rides, many=True)
                return Response(serializer.data)
                
            except ValueError:
                pass  # Invalid lat/lon values, fall back to normal list
        
        # Default list behavior
        return super().list(request, *args, **kwargs)


class RideEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RideEvent model
    """
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
