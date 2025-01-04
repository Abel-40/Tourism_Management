from users.models import User,UserProfile,TourGuider
from django.urls import reverse
from rest_framework import serializers
from .booking_serializer import BookingSerializer
from bookings.models import Booking
class UserProfileSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = UserProfile
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  userprofile = UserProfileSerializer(many=False,read_only=True)
  book_history = BookingSerializer(many=True,read_only=True)
  detail_url = serializers.SerializerMethodField()
  class Meta:
    model = User
    fields = ['email','username','first_name','last_name','password','userprofile']
    read_only_fields = ('book_history','detial_url','book_history')
  def validate(self, attrs):
    if not attrs.get('password'):
     return serializers.ValidationError("please enter a password")
   
  def get_detail_url(self,obj):
    return reverse('user-detail',args=[obj.slug])
    
class TourGuiderSerializer(serializers.ModelSerializer):
    confirmed_bookings = serializers.SerializerMethodField()
    class Meta:
        model = TourGuider
        fields = '__all__'

    def get_confirmed_bookings(self, obj):
        assigned_package_ids = obj.assigned_packages.values_list('id', flat=True)
        
        confirmed_bookings = Booking.confirmed_bookings.filter(package__id__in=assigned_package_ids)
     
        return confirmed_bookings.values('user__username', 'user__email', 'package__package_name')
