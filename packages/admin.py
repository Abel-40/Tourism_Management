from django.contrib import admin
from .models import Packages,SubPackages,PackageReview

# Register your models here.
class PackagesAdmin(admin.ModelAdmin):
  list_display = ('id','package_name','package_description','price','days_of_tour','start_date','created','publish','updated','created_by','status','location','weather','landscape')
  fields = ('package_name', 'package_description', 'price', 'days_of_tour', 'start_date', 'created_by', 'status', 'location', 'weather', 'landscape')
  readonly_fields = ('created', 'updated', 'publish')
  list_filter = ('status', 'location', 'created', 'updated')
  search_fields = ('package_name', 'location')  


admin.site.register(Packages,PackagesAdmin)
admin.site.register(SubPackages)
admin.site.register(PackageReview)