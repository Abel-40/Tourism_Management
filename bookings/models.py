from django.db import models
from packages.models import Packages
from users.models import User,TourGuider
# Create your models here.

class Booking(models.Model):
  class ConfirmedBookings(models.Manager):
    def get_queryset(self):
      return super().get_queryset().filter(status = Booking.Status.CONFIRMED)
  
  class Status(models.TextChoices):
    PENDING = 'Pending','PENDING'
    CONFIRMED = 'Confirmed','CONFIRMED'
    CANCELED = 'Canceled','CANCELED'
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='book_history')
  package = models.ForeignKey(Packages,on_delete=models.CASCADE,related_name='booked_packages')
  booking_date = models.DateTimeField(auto_now_add=True)
  number_of_people = models.PositiveIntegerField()
  total_price = models.DecimalField(max_digits=10,decimal_places=2)
  status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
  objects = models.Manager()
  confirmed_bookings = ConfirmedBookings()
  def save(self, *args, **kwargs):
    package_price = self.package.price
    self.total_price = self.number_of_people * package_price
    return super().save(*args,**kwargs)
  
  def __str__(self):
    return f"{self.user.username} Book package {self.package.package_name}"