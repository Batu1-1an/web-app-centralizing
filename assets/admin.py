from django.contrib import admin
from .models import Asset, Profile


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["name", "asset_type", "vendor", "expiry_date", "associated_user", "associated_department"]
    list_filter = ["asset_type", "associated_department"]
    search_fields = ["name", "vendor"]
    date_hierarchy = "expiry_date"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]
    list_filter = ["role"]
    search_fields = ["user__username", "user__email"]
