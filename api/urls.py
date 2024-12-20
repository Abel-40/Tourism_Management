from django.urls import path, include
from rest_framework.routers import DefaultRouter
from packages.views import PackageViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
