from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
import uuid
from django.utils.text import slugify
from packages.models import Packages

# Create your models here.

class UserManger(BaseUserManager):
  def create_user(self,email,password,username):
    if email is None:
      raise ValueError('Email required')
    
    email = self.normalize_email(email)
    user = self.model(email=email,username=username)
    user.set_password(password)
    user.save(using=self._db)
    return user
  def create_superuser(self,email,password,username):
    user = self.create_user(email=email,password=password,username=username)
    user.is_staff = True
    user.is_superuser = True
    user.save(using= self._db)
    return user
  
  
class User(AbstractUser):
  email = models.EmailField(unique=True,max_length=200)
  username = models.CharField(max_length=100,unique=False)
  slug = models.SlugField(unique=True,max_length=100)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['username']
  objects= UserManger()
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(f"{self.username}-{uuid.uuid4().hex[:8]}")
    super().save(*args,**kwargs)
  
  def __str__(self):
    return self.username
  
  
class UserProfile(models.Model):
  class CustomerManager(models.Manager):
    def get_queryset(self):
      return super().get_queryset().filter(role = UserProfile.Role.CUSTOMER)
  
  class Role(models.TextChoices):
    ADMIN = 'AD','Admin'
    CUSTOMER = 'CU','Customer'
    TOUR_STAFF = 'TS','Tour_Staff'
    TOUR_GUIDER = 'Tg','Tour_Guider'
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  address = models.CharField(max_length=200)
  profile_picture = models.ImageField(upload_to='profile_pictures/',null=True,blank=True)
  phone_number = models.CharField(max_length=13)
  role = models.CharField(max_length=2,choices=Role.choices,default=Role.CUSTOMER)
  #custom object to filter only Customers and default object
  
  objects = models.Manager()
  customers = CustomerManager()
  
  def __str__(self):
    return self.user.username
  
  
class TourGuider(models.Model) :
  user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='tour_guider')
  assigned_packages = models.ManyToManyField(Packages,related_name='tour_guiders')
  note = models.TextField()
  objects = models.Manager()
  
  def save(self, *args, **kwargs):
    if self.user_profile.role != UserProfile.Role.TOUR_GUIDER:
        self.user_profile.role = UserProfile.Role.TOUR_GUIDER
        self.user_profile.save(update_fields=['role'])  # Save only the role field
    super().save(*args, **kwargs)
 

    
  def __str__(self):
    return self.user_profile.user.username