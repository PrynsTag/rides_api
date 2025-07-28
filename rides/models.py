from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """
    Custom User model based on the requirements
    """
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50, default='user')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Ride(models.Model):
    """
    Ride model as per requirements
    """
    STATUS_CHOICES = [
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    id_rider = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='rides_as_rider',
        db_column='id_rider'
    )
    id_driver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='rides_as_driver',
        db_column='id_driver'
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
    
    class Meta:
        db_table = 'ride'
        indexes = [
            models.Index(fields=['pickup_time']),
            models.Index(fields=['status']),
            models.Index(fields=['id_rider']),
            models.Index(fields=['id_driver']),
        ]

    def __str__(self):
        return f"Ride {self.id_ride}: {self.status}"


class RideEvent(models.Model):
    """
    RideEvent model as per requirements
    """
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride, 
        on_delete=models.CASCADE, 
        related_name='ride_events',
        db_column='id_ride'
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ride_event'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['id_ride', 'created_at']),
        ]

    def __str__(self):
        return f"Event {self.id_ride_event}: {self.description}"
