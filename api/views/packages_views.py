from rest_framework import viewsets
from ..serializers.packages_serializers import (
  PackageSerializer,
  Packages,
  SubPackagesSerializers,
  SubPackages,
  PackageReviewSerializer,
  PackageReview
)

class PackagesApiViews(viewsets.ModelViewSet):
  queryset = Packages.published.all()
  serializer_class = PackageSerializer
  

class SubPackageApiView(viewsets.ModelViewSet):
  queryset = SubPackages.objects.all()
  serializer_class = SubPackagesSerializers
  
class PackageReviewApiView(viewsets.ModelViewSet):
  queryset = PackageReview.objects.all()
  serializer_class = PackageReviewSerializer