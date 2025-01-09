from rest_framework import viewsets,status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
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
  TourGuider,
  UserDetailSerializer,
  RoleAssignSerializer,
  UpdateUserInfoSerializer,
  UpadateUserProfileSerializer,
  UserDeletionSerializer,
  
  )
from django.shortcuts import get_object_or_404
from users.views import send_welcome_email
class UserApiView(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'slug'
  
class UserProfileApiView(viewsets.ModelViewSet):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  parser_classes = [MultiPartParser]
  
  
class TourGuiderApiView(viewsets.ModelViewSet):
  queryset = TourGuider.objects.all()
  serializer_class = TourGuiderSerializer
  
  
class UserCreationApiView(viewsets.ViewSet):
    lookup_field = 'slug'
    @action(detail=False, methods=['post'],permission_classes=[AllowAny],authentication_classes=[])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            if User.objects.filter(email=email).exists():
                return Response(
                    {"message": "Account exists, please sign in"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if send_welcome_email(email, username):
                serializer.save()
                return Response(
                    {"message": "Account created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"timeout": "Please check your internet connection"},
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_users(self, request):
        if request.user.is_superuser or request.user.userprofile.role == UserProfile.Role.TOUR_STAFF :
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        else:
            user = User.objects.get(email = request.user.email)
            serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def retrieve_user(self, request, slug=None):
        try:
            user = User.objects.get(slug=slug)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], permission_classes=[IsAdminUser])
    def assign_role(self, request):
        serializer = RoleAssignSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            role = serializer.validated_data['role']
            user = get_object_or_404(User, email=email)
            
            role_mapping = {
                'TS': UserProfile.Role.TOUR_STAFF,
                'AD': UserProfile.Role.ADMIN,
                'CU': UserProfile.Role.CUSTOMER,
                'TG': UserProfile.Role.TOUR_GUIDER
            }
            user.userprofile.role = role_mapping[role]
            user.userprofile.save()  
            if role_mapping[role] ==  UserProfile.Role.TOUR_GUIDER:
                if not user.userprofile.role == UserProfile.Role.TOUR_GUIDER:
                    TourGuider.objects.create(user_profile=user.userprofile)
                else:
                    return Response({"message": "user already have this role"}, status=status.HTTP_200_OK)
            return Response({"message": f"you give {role_mapping[role]} role to {user.username} successfully!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['patch'],permission_classes=[IsAuthenticated])
    def update_user_info(self,request):
        user = get_object_or_404(User,email = request.user.email)
        serializer = UpdateUserInfoSerializer(user,data= request.data,partial=True)
        if serializer.is_valid():
            password = serializer.validated_data.pop('password',None)
            if password:
                user.set_password(password)
            serializer.save()
            return Response({"message": "User updated successfully!"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False,methods=['patch'],permission_classes=[IsAuthenticated])
    def update_userprofile_info(self,request):
        user = get_object_or_404(User,email = request.user.email)
        userprofile = get_object_or_404(UserProfile,user = user)
        serializer = UpadateUserProfileSerializer(userprofile,data= request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "UserProfile updated successfully!"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
         

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        serializer = UserDeletionSerializer(data=request.data)
        print(f"Authenticated user: {request.user}")
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = request.user
            if not user.check_password(password):
                return Response({'message': 'Please enter the correct password'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.delete()  
            return Response({'message': 'User account deleted successfully!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def get_tourstaffs(self, request):
        tourstaffs = User.objects.filter(userprofile__role=UserProfile.Role.TOUR_STAFF)
        serializer = UserSerializer(tourstaffs, many=True)  # Ensure you pass `many=True`
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def get_customers(self, request):
        customers = User.objects.filter(userprofile__role=UserProfile.Role.CUSTOMER)
        serializer = UserSerializer(customers, many=True)  # Ensure you pass `many=True`
        return Response(serializer.data, status=status.HTTP_200_OK)


