from packages.models import Packages,SubPackages,PackageReview
from rest_framework import serializers

class SubPackagesSerializers(serializers.ModelSerializer):
  
  class Meta:
    model =SubPackages
    fields = '__all__'
    
    
class PackageReviewSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = PackageReview
    fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
  
  subpackages = SubPackagesSerializers(many=True,read_only=True)
  package_review = PackageReviewSerializer(many=True,read_only=True)
  class Meta:
    model = Packages
    fields= [
      'package_name',
      'package_description',
      'price',
      'days_of_tour',
      'start_date',
      'created',
      'publish',
      'updated',
      'created_by',
      'status',
      'location',
      'weather',
      'landscape',
      'subpackages',
      'package_review'
      ]#only to display to add not all attributes are not needed (publish,created,updated,subpackages) are not needed to create pakcages
