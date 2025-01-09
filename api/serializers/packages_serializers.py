from packages.models import Packages,SubPackages,PackageReview,PackageImages
from rest_framework import serializers
from django.utils import timezone
from ..serializers.user_serializers import TourGuider
class PackageImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = PackageImages
    fields = ['image','caption']

class SubPackagesSerializers(serializers.ModelSerializer):
  class Meta:
    model =SubPackages
    fields = '__all__'
class PackageReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageReview
        fields = ('package', 'rate', 'comment')
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user 
        return super().create(validated_data)

class PackageSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    package_images = PackageImageSerializer(many=True)
    
    class Meta:
        model = Packages
        fields = (
            'package_name',
            'package_description',
            'price',
            'days_of_tour',
            'start_date',
            'location',
            'weather',
            'landscape',
            'package_images',
            'detail_url',
        )
        read_only_fields = ('detail_url',)

        
    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request') and self.context['request'].method in ['POST', 'PATCH']:
            fields.pop('detail_url', None)
        return fields
    
    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['created_by'] = user 
        images_data = validated_data.pop('package_images', [])
        package = Packages.objects.create(**validated_data)
        for image_data in images_data:
            PackageImages.objects.create(package=package, **image_data)
        return package   
    def update(self, instance, validated_data):
        images_data = validated_data.pop('package_images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data:
            instance.package_images.all().delete()
            for image_data in images_data:
                PackageImages.objects.create(package=instance, **image_data)
        return instance

    def validate(self, attrs):
        package_start_date = attrs.get('start_date')
        if package_start_date and package_start_date < timezone.now().date():
            raise serializers.ValidationError("Package start date can't be in the past.")
        return attrs
    
    def get_detail_url(self, obj):
        return obj.get_absolute_url()
    
class PackageDetailSerializer(serializers.ModelSerializer):
    subpackages = SubPackagesSerializers(many=True, read_only=True)
    package_review = PackageReviewSerializer(many=True, read_only=True)
    package_images = PackageImageSerializer(many=True, read_only=True)
    class Meta:
        model = Packages
        fields = (
            'package_name',
            'package_description',
            'price',
            'days_of_tour',
            'start_date',
            'location',
            'weather',
            'landscape',
            'package_images',
            'package_review',
            'subpackages'
        )
        read_only_fields = (
            'created_by',
            'status',
            'created',
            'publish',
            'updated',
            'package_images',
            'package_review',
            'sub_packages'
        )
        
class PackagePublisherSerializer(serializers.Serializer):
    package_slug = serializers.SlugField(max_length = 130)
    tourguider_email = serializers.EmailField(max_length = 150)

class TourGuiderPackagesSerializer(serializers.ModelSerializer):
    assigned_packages = serializers.StringRelatedField(many=True) 
    class Meta:
        model = TourGuider
        fields = ['assigned_packages']
