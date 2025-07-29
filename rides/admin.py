from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Ride, RideEvent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for User model
    """
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'first_name', 'last_name', 'email')}),
    )


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    """
    Admin configuration for Ride model
    """
    list_display = ('id_ride', 'status', 'id_rider', 'id_driver', 'pickup_time')
    list_filter = ('status', 'pickup_time')
    search_fields = ('id_rider__email', 'id_driver__email')
    readonly_fields = ('id_ride',)
    
    fieldsets = (
        ('Ride Information', {
            'fields': ('id_ride', 'status', 'pickup_time')
        }),
        ('People', {
            'fields': ('id_rider', 'id_driver')
        }),
        ('Locations', {
            'fields': (
                ('pickup_latitude', 'pickup_longitude'),
                ('dropoff_latitude', 'dropoff_longitude')
            )
        }),
    )


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    """
    Admin configuration for RideEvent model
    """
    list_display = ('id_ride_event', 'id_ride', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description', 'id_ride__id_ride')
    readonly_fields = ('id_ride_event', 'created_at')
