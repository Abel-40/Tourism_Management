from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from ..serializers.user_serializers import (
  UserSerializer,
  User,
  UserProfileSerializer,
  UserProfile,
  TourGuiderSerializer,
  TourGuider
  )
from users.views import send_welcome_email

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
  
  
class UserCreationApiView(viewsets.ViewSet):
  @action(detail=False,methods=['post'])
  def signup(self,request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
      email = serializer.validated_data['email']
      username = serializer.validated_data['username']
      if User.objects.filter(email=email).exists():
        return Response({"message":"account existed please sign in"},status=status.HTTP_403_FORBIDDEN)
      
      send_welcome_email(email,username)
      if send_welcome_email(email,username):
        serializer.save()
        return Response({"message":"account created successfully"},status=status.HTTP_201_CREATED)
      else:
        return Response({"timeout":"please check your internet connection"},status=status.HTTP_408_REQUEST_TIMEOUT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # def delete(self,request):
  #   serial