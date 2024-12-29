from rest_framework import viewsets,status
from rest_framework.views import APIView
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
  
  
class UserCreationApiView(APIView):
  def post(self,request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
      email = serializer.validated_data['email']
      if User.objects.filter(email=email).exists():
        return Response({"message":"account existed please sign in"},status=status.HTTP_403_FORBIDDEN)
      user = serializer.save()
      send_welcome_email(email,user.username)
      return Response({"message":"account created successfully"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
