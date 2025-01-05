from rest_framework import serializers
from bookings.models import Booking
from django.utils import timezone
from django.urls import reverse
class BookingPaymentSerializer(serializers.Serializer):
  package_name = serializers.CharField(max_length=100)
  pin = serializers.CharField(max_length=4)

class BookingSerializer(serializers.ModelSerializer):
  detail_url = serializers.SerializerMethodField()
  class Meta:
    model = Booking
    fields = ('user','package','number_of_people','status','total_price','booking_date','detail_url')
    read_only_fields = ('user','total_price','status','booking_date','detail_url')
    
  def validate(self, attrs):
    package = attrs.get('package')
    
    if package.start_date < timezone.now().date():
        raise serializers.ValidationError("Package start date has already passed.")
    return attrs
  def get_detail_url(self,obj):
    return reverse('booking-detial',args=[obj.slug])

  