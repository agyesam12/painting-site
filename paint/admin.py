from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin

admin.site.register(User),
admin.site.register(Service),
admin.site.register(Portfolio),
admin.site.register(Testimonial),
admin.site.register(ContactRequest),
admin.site.register(EstimateRequest),
admin.site.register(Notification),
admin.site.register(FAQ),
admin.site.register(LogEntry)

