from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User),
admin.site.register(Service),
admin.site.register(Portfolio),
admin.site.register(Testimonial),
admin.site.register(ContactRequest),
admin.site.register(EstimateRequest),
admin.site.register(Notification)
