from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import (AbstractBaseUser)
from django.contrib.auth.models import User, Group
from .managers import UserManager
from django.conf import settings
from django.db import models
import datetime

def profile_upload_path(instance, filename):
    return 'profile_image/{0}/{1}'.format(instance.id, filename)

def place_upload_path(instance, filename):
    return 'place/{0}/{1}'.format(instance.place, filename)

class Province(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        name ='%s' % (self.name)
        return name.strip()
    verbose_name_plural="Province"

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    def __str__(self):
        name ='%s' % (self.name)
        return name.strip()
    class Meta:
        verbose_name_plural="Cities"

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    sex_choices = (('Male', 'Male'),('Female', 'Female'),)

    first_name = models.CharField(('First Name'),max_length=255)
    middle_name = models.CharField(('Middle Name'),max_length=255,blank=True, null=True)
    last_name = models.CharField(('Last Name'),max_length=255)
    suffix = models.CharField(('Suffix'),max_length=255, blank=True)
    sex = models.CharField(('Sex'), max_length=10, choices=sex_choices)
    birthdate = models.DateField(('Birth date'), help_text='Format: yyyy-mm-dd', null=True)
    address = models.CharField(('Address'), max_length=255, blank=True, null=True, help_text='Apartment, suite, unit, building, floor, street, barangay')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City/Municipality', null=True)

    contact_number = models.CharField(('Contact Number'), max_length=20)
    travel_history = models.CharField(('Travel History'), max_length=500, blank=True, null=True)
    image = models.ImageField(default="user.png", upload_to=profile_upload_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    objects = UserManager()

    def full_name(self):
       full_name = '%s %s %s %s' % (self.first_name, self.middle_name, self.last_name, self.suffix)
       return full_name.strip()

    def get_age(self):
        date=datetime.date.today()-self.birthdate
        return date

    def get_short_name(self):
        name= '%s %s' % (self.first_name,self.last_name)
        return name.strip()

    def get_email(self):              
        return self.email

    def __str__(self):
        flname ='%s %s' % (self.first_name, self.last_name)
        return flname.strip()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    @property
    def staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def superuser(self):
        "Is the user a superuser?"
        return self.is_superuser

    @property
    def active(self):
        "Is the user active?"
        return self.is_active

class Place(models.Model):
    place = models.CharField(max_length=255)
    address = models.CharField(('Address'), max_length=255, blank=True, null=True, help_text='Apartment, suite, unit, building, floor, street, barangay')
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(default="place.png",upload_to=place_upload_path)

    def __str__(self):
        return self.place

class CheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    checkin_place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name="now", )
    x = [('Home','Home'), ('Others','Others')]
    recent_place = models.CharField(("Recent place that have you been"),max_length=255, choices=x)
    recent_location = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name="recent" )
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user


