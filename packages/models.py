from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
# from users.models import User
# Create your models here.

class Packages(models.Model):
  
  class Status(models.TextChoices):
    PUBLISHED = 'PB','Publish'
    DRAFT = 'DR','Draft'
  class PublishedManager(models.Manager):
    def get_queryset(self):
      return super().get_queryset().filter(status = Packages.Status.PUBLISHED)
  
  
  package_name = models.CharField(unique=True,max_length=250)
  package_description = models.TextField()
  price = models.DecimalField(max_digits=10,decimal_places=2)
  days_of_tour = models.PositiveIntegerField()
  start_date = models.DateField()
  created = models.DateTimeField(auto_now_add=True)
  publish = models.DateTimeField(default= timezone.now)
  updated = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='Packages')
  status = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT)
  location = models.CharField(max_length=100)
  weather = models.CharField(max_length=100)
  landscape = models.CharField(max_length=100)
  slug = models.SlugField(unique=True,max_length=100)

  def save(self,*args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.package_name)
    super().save(*args,**kwargs)
  
  
  objects = models.Manager()
  published = PublishedManager()
  
  class Meta:
    ordering = ['-publish']
    indexes = [
      models.Index(fields=['-publish'])
    ]
  def __str__(self):
    return self.package_name
  
  def get_absolute_url(self):
      return reverse("package-detail", kwargs={"slug":self.slug})
  
  
  
class PackageImages(models.Model) :
  package = models.ForeignKey(to=Packages,on_delete=models.CASCADE,related_name='package_images')
  image = models.ImageField(upload_to='package_image/')
  caption = models.CharField(max_length=255,blank=True,null=True)

  def __str__(self):
    return f"Image for {self.package.package_name}"
  
class SubPackages(models.Model):
    subpackage_name = models.CharField(max_length=100)
    subpackage_description = models.TextField()
    package = models.ForeignKey(to=Packages,on_delete=models.CASCADE,related_name='subpackages')
    subpackage_image = models.ImageField(upload_to='subpackage_image/',blank=True,null=True)
    
  
    def __str__(self):
      return self.subpackage_name
    
    
class PackageReview(models.Model):
  RATING_CHOICES = [(i,str(i)) for i in range(1,5)]
  user = models.ForeignKey(to='users.User',on_delete=models.CASCADE,related_name='user_review')
  package = models.ForeignKey(to=Packages,on_delete=models.CASCADE,related_name='package_review')
  rate = models.IntegerField(choices=RATING_CHOICES)
  comment = models.TextField()
  
  def __str__(self):
    return f"{self.user.username} rated {self.package.package_name} package"