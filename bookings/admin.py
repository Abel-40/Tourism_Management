from django.contrib import admin
from bookings.models import Booking
# Register your models here.

class BookingAdminDisplay(admin.ModelAdmin):
  fields = ('user','package','number_of_people','status')
  list_display = ('user','package','number_of_people','total_price','status','slug')
admin.site.register(Booking,BookingAdminDisplay)