from rest_framework import serializers
from bookings.models import Booking

class BookingPaymentSerializer(serializers.Serializer):
  package_name = serializers.CharField(max_length=100)
  pin = serializers.CharField(max_length=4)

class BookingSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Booking
    fields = ('user','package','number_of_people','status','total_price')
    read_only_fields = ('total_price',)