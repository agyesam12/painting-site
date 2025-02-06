from django.db import models
from django.contrib.auth.models import AbstractUser
from packages.integerId import IntegerIDField
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import now
import random
# Create your models here.

SERVICE_CATEGORIES = (
    ('Residential', 'Residential'),
    ('Commercial', 'Commercial'),
    ('Industrial', 'Industrial'),
    ('Historical', 'Historical'),
)

ESTIMATE_STATUS = (
    ('Pending', 'Pending'),
    ('Reviewed', 'Reviewed'),
    ('Approved', 'Approved'),
)


class User(AbstractUser):
    user_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    full_name = models.CharField(max_length=60, null=True, blank=True)
    photo = ResizedImageField(size=[500, 500], default='media/user.jpg', upload_to='users/')
    phone_number = models.CharField(max_length=20, blank=False, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    email = models.EmailField(blank=False, unique=True, null=True)
    is_user = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    bio = CKEditor5Field(config_name='extends', max_length=200, blank=True, default="Hi there,...")
    # Agent can enable/disable payment methods
    otp = models.CharField(max_length=4, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class Service(models.Model):
    """Represents different types of painting services."""
    service_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    portfolio_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    before_image = models.ImageField(upload_to='portfolio/before/')
    after_image = models.ImageField(upload_to='portfolio/after/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Testimonial(models.Model):
    testimonial_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Rating out of 5
    status = models.BooleanField(default=False)  # False means not approved yet
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} ★"
    

class ContactRequest(models.Model):
    contact_request_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.email}"
    

class EstimateRequest(models.Model):
    estimate_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='estimates')
    details = models.TextField()
    status = models.CharField(max_length=20, choices=ESTIMATE_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Estimate for {self.service_type.name} by {self.name}"