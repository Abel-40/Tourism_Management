from django.contrib import admin
from .models import User,UserProfile,TourGuider
# Register your models here.

class UserDisplay(admin.ModelAdmin):
  list_display = ('id','email','username','first_name','last_name','slug')
  fields = ('email','username','password','first_name','last_name')
  readonly_fields = ('slug',)
  def get_queryset(self, request):
    return super().get_queryset(request)
admin.site.register(User,UserDisplay)

class UserProfileDisplay(admin.ModelAdmin):
  list_display = ('user','address','profile_picture','phone_number','role')



admin.site.register(TourGuider)
admin.site.register(UserProfile,UserProfileDisplay)