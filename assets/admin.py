from django.contrib import admin
from .models import Asset, Profile

# Basic registration for now
# We can customize the admin display later if needed
admin.site.register(Asset)
admin.site.register(Profile)
