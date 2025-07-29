import django_filters
from django.db.models import Q
from .models import Ride


class RideFilter(django_filters.FilterSet):
    """
    Filter for Ride model supporting status and rider email filtering
    """
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    rider_email = django_filters.CharFilter(method='filter_rider_email')
    
    class Meta:
        model = Ride
        fields = ['status', 'rider_email']
    
    def filter_rider_email(self, queryset, name, value):
        """
        Filter rides by rider's email address
        """
        return queryset.filter(id_rider__email__icontains=value)
