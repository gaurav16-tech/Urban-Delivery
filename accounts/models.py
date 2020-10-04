from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django import forms


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):


    status = [
        ('1', 'OPEN'),
        ('2', 'CLOSED'),
    ]
    Name = models.CharField(max_length=200)
    Address = models.TextField(blank=True)
    City = models.CharField(max_length=100, default = 'None')
    State = models.CharField(max_length=100, default = 'None')
    Pincode = models.IntegerField(blank=True, null=True)
    MobileNumber = models.CharField(max_length=200)
    ShipmentWeight = models.DecimalField( max_digits = 5, decimal_places = 2, default = '00.00')
    Origin = models.TextField(blank=True)
    Destination = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    Status = models.CharField(max_length=100,choices=status,default='OPEN')
    ShipmentDate = models.DateTimeField(default=timezone.now, null=True)
    deliveryperson = models.CharField(max_length=200, default='None')
    Totalamount = models.DecimalField( max_digits = 5, decimal_places = 2, default = '00.00')
    Uploadimage = models.ImageField(upload_to ='static/mechit/images/', null=True, blank = True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.Name



class DeliveryPerson(models.Model):

    user = models.CharField(max_length=200)
    PhoneNo = models.CharField(max_length=200)
    Address = models.TextField(blank=True)
    City = models.CharField(max_length=100, default = 'None')
    State = models.CharField(max_length=100, default = 'None')
    Pincode = models.IntegerField(blank=True, null=True)
    picture = models.FileField(upload_to = "pictures/")

    def __str__(self):
        return self.user

class Administration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
