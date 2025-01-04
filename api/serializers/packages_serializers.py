from packages.models import Packages,SubPackages,PackageReview,PackageImages
from rest_framework import serializers
from django.urls import reverse
from django.utils import timezone
class PackageImageSerializer(serializers.ModelSerializer):
  class Meta:
    fields = '__all__'

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
  detial_url = serializers.SerializerMethodField()
  package_image = PackageImageSerializer(many=True,read_only=True)
  package_review = PackageReviewSerializer(many=True,read_only=True)
  class Meta:
    model = Packages
    fields= (
      'package_name',
      'package_description',
      'price',
      'days_of_tour',
      'start_date',
      'location',
      'weather',
      'landscape',
      'subpackages'
      )#only to display to add not all attributes are not needed (publish,created,updated,subpackages) are not needed to create pakcages
    read_only_fields = (
      'created_by',
      'status',
      'created',
      'publish',
      'updated',
      'package_review',
      'detial_url',
      'package_image'
      )
  def get_detail_url(self,obj):
    return reverse('package-detial',args=[obj.slug])
  
  def validate(self, attrs):
    package_start_date = attrs.get('start_date')
    if package_start_date < timezone.now().date():
        raise serializers.ValidationError("Package start date can't be in the past.")