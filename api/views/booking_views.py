from ..serializers.booking_serializer import BookingSerializer,Booking
from rest_framework import viewsets

class BookingApiView(viewsets.ModelViewSet):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer