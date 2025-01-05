from users.models import User,UserProfile,TourGuider
from django.urls import reverse
from rest_framework import serializers
from .booking_serializer import BookingSerializer
from bookings.models import Booking
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['user','address','profile_picture','phone_number']
    read_only_fields = ('user')

class UserSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Correct field name
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'detail_url',  # Corrected field name
        ]
        read_only_fields = ( 'detail_url')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user
    def validate(self, attrs):
        if not attrs.get('password'):
            raise serializers.ValidationError("Please enter a password")
        return attrs

    def get_detail_url(self, obj):
        return obj.get_absolute_url()
    
class TourGuiderSerializer(serializers.ModelSerializer):
    confirmed_bookings = serializers.SerializerMethodField()
    class Meta:
        model = TourGuider
        fields = '__all__'

    def get_confirmed_bookings(self, obj):
        assigned_package_ids = obj.assigned_packages.values_list('id', flat=True)
        
        confirmed_bookings = Booking.confirmed_bookings.filter(package__id__in=assigned_package_ids)
     
        return confirmed_bookings.values('user__username', 'user__email', 'package__package_name')

class UserDetailSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)  # Explicitly read-only
    book_history = BookingSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = (             
            'email',
            'username',
            'first_name',
            'last_name',
            'userprofile',
            'book_history',
        )
        read_only_fields = fields  # All fields are read-only


class RoleAssignSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length=150)
    role = serializers.CharField(max_length=200)
    def validate(self, attrs):
        role = ['AD','TS','TG','CU']
        if not attrs.get('role')  in role:
            raise serializers.ValidationError({
                "role": f"Invalid role. Available roles are: \n AD = Admin \n TS = Tourstaff \n TG = TourGuider \n CU = Customer"})
        return attrs
    
class UpdateUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name']

    def validate(self, attrs):
        if 'email' in attrs:
            raise serializers.ValidationError({"error": "Email field can't be updated. Please try updating other fields."})
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('email', None)
        return super().update(instance, validated_data)

class UpadateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address','profile_picture','phone_number','role']
    def validate(self, attrs):
        if 'role' in attrs:
            raise serializers.ValidationError({"error": "There is no field called role. Please try again."})
        return attrs
    def update(self, instance, validated_data):
        validated_data.pop('role',None)
        return super().update(instance,validated_data)