from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RideViewSet, RideEventViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideEventViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
