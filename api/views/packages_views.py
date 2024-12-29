from rest_framework import viewsets
from rest_framework.response import Response
from ..serializers.packages_serializers import (
  PackageSerializer,
  Packages,
  SubPackagesSerializers,
  SubPackages,
  PackageReviewSerializer,
  PackageReview
)
from rest_framework.views import APIView
class PackagesApiViews(viewsets.ModelViewSet):
  queryset = Packages.published.all()
  serializer_class = PackageSerializer
  

class SubPackageApiView(viewsets.ModelViewSet):
  queryset = SubPackages.objects.all()
  serializer_class = SubPackagesSerializers
  
class PackageReviewApiView(viewsets.ModelViewSet):
  queryset = PackageReview.objects.all()
  serializer_class = PackageReviewSerializer

class GetPakcages(APIView):
  def get(self,request):
    queryset = Packages.published.all()
    serializer = PackageSerializer(data=queryset)
    return Response(serializer.data)