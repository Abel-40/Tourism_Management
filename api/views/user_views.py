from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from ..serializers.user_serializers import (
  UserSerializer,
  User,
  UserProfileSerializer,
  UserProfile,
  TourGuiderSerializer,
  TourGuider
  )

class UserApiView(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
  
class UserProfileApiView(viewsets.ModelViewSet):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  parser_classes = [MultiPartParser]
  
  
class TourGuiderApiView(viewsets.ModelViewSet):
  queryset = TourGuider.objects.all()
  serializer_class = TourGuiderSerializer