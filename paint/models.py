from django.db import models
from django.contrib.auth.models import AbstractUser
from packages.integerId import IntegerIDField
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta
from django.utils.timezone import now
import random

# Service and Estimate Categories
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

# User Model
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
    otp = models.CharField(max_length=4, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

# Service Model
class Service(models.Model):
    service_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    image = models.ImageField(upload_to='services/')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')

    def __str__(self):
        return self.name

# Portfolio Model
class Portfolio(models.Model):
    portfolio_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    before_image = models.ImageField(upload_to='portfolio/before/')
    after_image = models.ImageField(upload_to='portfolio/after/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='portfolios')

    def __str__(self):
        return self.title

# Testimonial Model
class Testimonial(models.Model):
    testimonial_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Rating out of 5
    status = models.BooleanField(default=False)  # False means not approved yet
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} ★"

# Contact Request Model
class ContactRequest(models.Model):
    contact_request_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.email}"

# Estimate Request Model
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

# Notification Model
class Notification(models.Model):
    notification_id = IntegerIDField(unique=True, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}"

# Signal to create notifications
@receiver(post_save, sender=ContactRequest)
def create_contact_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming a single site owner for simplicity
        site_owner = User.objects.filter(is_admin=True).first()
        if site_owner:
            Notification.objects.create(
                user=site_owner,
                message=f"New contact request from {instance.name}"
            )

@receiver(post_save, sender=EstimateRequest)
def create_estimate_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming a single site owner for simplicity
        site_owner = User.objects.filter(is_admin=True).first()
        if site_owner:
            Notification.objects.create(
                user=site_owner,
                message=f"New estimate request for {instance.service_type.name} by {instance.name}"
            )
