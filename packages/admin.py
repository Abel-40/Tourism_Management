from django.contrib import admin
from .models import Packages,SubPackages,PackageReview,PackageImages

# Register your models here.
class PackagesAdmin(admin.ModelAdmin):
  list_display = ('id','package_name','package_description','price','days_of_tour','start_date','created','publish','updated','created_by','status','location','weather','landscape','slug')
  fields = ('package_name', 'package_description', 'price', 'days_of_tour', 'start_date', 'created_by', 'status', 'location', 'weather', 'landscape')
  readonly_fields = ('created', 'updated', 'publish','slug')
  list_filter = ('status', 'location', 'created', 'updated')
  search_fields = ('package_name', 'location')  

class SubpackageAdmin(admin.ModelAdmin):
  list_display = ('id','package','subpackage_description','subpackage_image')
admin.site.register(Packages,PackagesAdmin)
admin.site.register(SubPackages,SubpackageAdmin)
admin.site.register(PackageReview)
admin.site.register(PackageImages)