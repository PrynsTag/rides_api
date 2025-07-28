from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import User, Ride, RideEvent


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number']


class RideEventSerializer(serializers.ModelSerializer):
    """
    Serializer for RideEvent model
    """
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    """
    Serializer for Ride model with related data
    """
    id_rider_data = UserSerializer(source='id_rider', read_only=True)
    id_driver_data = UserSerializer(source='id_driver', read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    
    class Meta:
        model = Ride
        fields = [
            'id_ride', 'status', 'id_rider', 'id_driver',
            'pickup_latitude', 'pickup_longitude',
            'dropoff_latitude', 'dropoff_longitude', 'pickup_time',
            'id_rider_data', 'id_driver_data', 'todays_ride_events'
        ]
    
    def get_todays_ride_events(self, obj):
        """
        Get ride events from the last 24 hours
        """
        # This will be optimized in the viewset using prefetch_related
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        events = getattr(obj, 'recent_events', obj.ride_events.filter(created_at__gte=twenty_four_hours_ago))
        return RideEventSerializer(events, many=True).data


class RideCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating rides
    """
    class Meta:
        model = Ride
        fields = [
            'status', 'id_rider', 'id_driver',
            'pickup_latitude', 'pickup_longitude',
            'dropoff_latitude', 'dropoff_longitude', 'pickup_time'
        ]
