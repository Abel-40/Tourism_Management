from django.db import models

class Package(models.Model):
    package_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    weather = models.CharField(max_length=50)
    landscape = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.package_name

class Booking(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    number_of_people = models.PositiveIntegerField()
    booking_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.package.price * self.number_of_people
        super().save(*args, **kwargs)
