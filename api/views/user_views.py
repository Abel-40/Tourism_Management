from rest_framework import viewsets,status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from bookings.permissions import IsTourGuider
from rest_framework.decorators import action,permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from packages.models import Packages
from ..serializers.user_serializers import (
  UserSerializer,
  User,
  UserProfile,
  TourGuiderSerializer,
  TourGuider,
  UserDetailSerializer,
  RoleAssignSerializer,
  UpdateUserInfoSerializer,
  UpadateUserProfileSerializer,
  UserDeletionSerializer
  
  )
from django.shortcuts import get_object_or_404
from users.views import send_welcome_email
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

        try:
            if send_welcome_email(email, username):
                self.perform_create(serializer)
                return Response({"message": "Account created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Please check your internet connection"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response({"message": f"Email sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.save()
        print('object saved to database')

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], authentication_classes=[])
    def signin(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Login successful.",
            },
            status=status.HTTP_200_OK,
        )

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




class TourGuiderViewSet(viewsets.ViewSet):
    permission_classes = [IsTourGuider]

    @action(detail=False, methods=['get'])
    def tg_packages_booking_confirmed_users(self, request):
        try:
            tour_guider = TourGuider.objects.get(user_profile=request.user.userprofile)
        except TourGuider.DoesNotExist:
            return Response({"error": "Tour Guider profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TourGuiderSerializer(tour_guider)
        return Response(serializer.data.get('confirmed_bookings'), status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def add_note(self, request):
        try:
            tour_guider = TourGuider.objects.get(user=request.user)
        except TourGuider.DoesNotExist:
            return Response({"error": "Tour Guider profile not found."}, status=status.HTTP_404_NOT_FOUND)

        package_id = request.data.get('package_id')
        note = request.data.get('note')

        if not package_id or not note:
            return Response({"error": "Both 'package_id' and 'note' are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            package = Packages.objects.get(id=package_id, assigned_to=tour_guider)
        except Packages.DoesNotExist:
            return Response({"error": "Package not found or not assigned to you."}, status=status.HTTP_404_NOT_FOUND)

        package.note = note
        package.save()

        return Response({"message": "Note added successfully."}, status=status.HTTP_200_OK)