from rest_framework import viewsets,status
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from bookings.permissions import IsAdminOrTourStaff,IsCustomer,IsTourGuider
from ..serializers.packages_serializers import (
  PackageSerializer,
  Packages,
  SubPackagesSerializers,
  SubPackages,
  PackageReviewSerializer,
  PackageDetailSerializer,
  PackagePublisherSerializer,
  TourGuiderPackagesSerializer
)
from ..serializers.user_serializers import TourGuider,User,UserProfile

class PackageApiView(viewsets.ViewSet):
  lookup_field = 'slug'
  @action(detail=False,methods=['get'],permission_classes=[AllowAny],authentication_classes=[])
  def get_packages(self,request):
    packages = Packages.published.all()
    serializer = PackageSerializer(packages,many=True,context={'request': request})
    return Response(serializer.data,status=status.HTTP_200_OK)
  

  @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
  def get_draft_packages(self, request):
      draft_packages = get_list_or_404(Packages,status=Packages.Status.DRAFT)
      serializer = PackageSerializer(draft_packages, many=True,context={'request': request})
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
  @action(detail=False,methods=['get'],permission_classes=[IsAuthenticated])
  def retrieve_package(self, request, slug=None):
        try:
            package = get_object_or_404(Packages,slug=slug)
            serializer = PackageDetailSerializer(package)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Packages.DoesNotExist:
            return Response({"error": "package not found"}, status=status.HTTP_404_NOT_FOUND)



  @action(detail=False, methods=['post'], permission_classes=[IsAdminOrTourStaff])
  def add_subpackages(self, request):
        serializer = SubPackagesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sub-package added successfully!'}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



  @action(detail=False, methods=['patch'], permission_classes=[IsAdminOrTourStaff])
  def update_subpackages(self, request):

      subpackage_id = request.data.get('id')
      subpackage = get_object_or_404(SubPackages,id=subpackage_id)
      serializer = SubPackagesSerializers(subpackage, data=request.data, partial=True)
      if serializer.is_valid():
          serializer.save()
          return Response({'message': 'Sub-package updated successfully!'}, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



  @action(detail=False, methods=['delete'], permission_classes=[IsAdminOrTourStaff])
  def delete_subpackages(self, request):
      subpackage_id = request.data.get('id')
      subpackage = get_object_or_404(SubPackages,id=subpackage_id)
      subpackage.delete()
      return Response({'message': 'Sub-package deleted successfully!'}, status=status.HTTP_200_OK)



  @action(detail=False,methods=['patch'],permission_classes=[IsAdminOrTourStaff])
  def update_packages(self,request):
    package_slug = request.data.get('slug')
    package = get_object_or_404(Packages,slug= package_slug)
    serializer = PackageDetailSerializer(package,data=request.data,partial=True,context={'request':request})
    if serializer.is_valid():
      serializer.save()
      return Response({'message':'package updated successfully!!!'},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
  
  
  @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
  def delete_packages(self, request):
      package_slug = request.data.get('slug')
      package = get_object_or_404(Packages,id=package_slug)
      package.delete()
      return Response({'message': 'Package deleted successfully!'}, status=status.HTTP_200_OK)



  @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
  def publish_Assign_Packages(self, request):
      serializer = PackagePublisherSerializer(data=request.data)
      if serializer.is_valid():
          slug = serializer.validated_data['package_slug']
          tour_guider_email = serializer.validated_data['tourguider_email']
          package = get_object_or_404(Packages, slug=slug, status=Packages.Status.DRAFT)
          user = get_object_or_404(User, email=tour_guider_email)
          if user.userprofile.role != UserProfile.Role.TOUR_GUIDER:
              return Response({'error': 'The user is not a tour guider! Please choose another user.'}, 
                              status=status.HTTP_400_BAD_REQUEST)
          tour_guider = get_object_or_404(TourGuider, user_profile=user.userprofile)
          tour_guider.assigned_packages.add(package)
          tour_guider.save()
          package.status = Packages.Status.PUBLISHED
          package.save()
          
          return Response({"success": f"Package published and assigned successfully to {tour_guider.user_profile.user.username}!"}, status=status.HTTP_200_OK)
      
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



  @action(detail=False,methods=['post'],permission_classes=[IsCustomer])
  def review_packages(self,request):
    serializer = PackageReviewSerializer(data = request.data,context={'request':request})
    if serializer.is_valid():
      serializer.save()
      return Response({"success": "Thanks for your review!"} ,status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  
  @action(detail=False, methods=['get'], permission_classes=[IsTourGuider])
  def tour_guiders_packages(self, request):
      userprofile = request.user.userprofile
      tour_guider = get_object_or_404(TourGuider, userprofile=userprofile)
      
      serializer = TourGuiderPackagesSerializer(tour_guider)
      return Response(serializer.data, status=status.HTTP_200_OK)

    
    