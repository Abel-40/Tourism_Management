from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views.user_views import TourGuiderViewSet,UserCreationApiView
from .views.packages_views import PackageApiView
from .views.bankist_view import BankistViewSet
from .views.booking_views import BookingApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
router = DefaultRouter()
router.register(r'user',UserCreationApiView,basename='user')
router.register(r'package',PackageApiView,basename='package')
router.register(r'bookings',BookingApiView,basename='booking')
router.register(r'bankist',BankistViewSet,basename='bankist')
router.register(r'tourguider',TourGuiderViewSet,basename='tourguider')

urlpatterns = [
  path('api/',include(router.urls)),
  path('user/<slug:slug>/', UserCreationApiView.as_view({'get': 'retrieve_user'}), name='user-detail'),
  path('package/<slug:slug>/', PackageApiView.as_view({'get': 'retrieve_package'}), name='package-detail'),
  path('booking/detial/<slug:slug>/', BookingApiView.as_view({'get': 'retrieve_booking'}), name='book-detail')
  
]


urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  
]