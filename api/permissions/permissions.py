from rest_framework.permissions import BasePermission
from users.models import UserProfile

class IsAdminOrTourStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            try:
                user_profile = user.userprofile 
                return user_profile.role in [
                    UserProfile.Role.ADMIN,
                    UserProfile.Role.TOUR_STAFF
                ]
            except UserProfile.DoesNotExist:
                return False
        return False
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            try:
                user_profile = user.userprofile 
                return user_profile.role == UserProfile.Role.CUSTOMER
            except UserProfile.DoesNotExist:
                return False
        return False
class IsTourGuider(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            try:
                user_profile = user.userprofile 
                return user_profile.role == UserProfile.Role.TOUR_GUIDER
            except UserProfile.DoesNotExist:
                return False
        return False       
class IsBookingOwner(BasePermission):
   def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            return user == obj.user
        return False