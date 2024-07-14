# assets/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Asset(models.Model):
    """Represents a trackable IT asset."""

    class AssetType(models.TextChoices):
        LICENSE = 'LIC', _('License')
        DOMAIN = 'DOM', _('Domain')
        SSL_CERTIFICATE = 'SSL', _('SSL Certificate')
        SOFTWARE_SUBSCRIPTION = 'SUB', _('Software Subscription')

    name = models.CharField(max_length=255, help_text="Name of the asset (e.g., 'Office 365 E3', 'example.com')")
    asset_type = models.CharField(
        max_length=3,
        choices=AssetType.choices,
        help_text="The type of the asset"
    )
    vendor = models.CharField(max_length=255, blank=True, help_text="Vendor or provider (e.g., 'Microsoft', 'GoDaddy')")
    expiry_date = models.DateField(help_text="Date the asset expires or needs renewal")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Annual or periodic cost")
    associated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep asset even if user is deleted, just remove association
        null=True,
        blank=True,
        help_text="Primary user associated with this asset"
    )
    associated_department = models.CharField(max_length=100, blank=True, help_text="Department associated with this asset")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_asset_type_display()}: {self.name}"

    class Meta:
        ordering = ['expiry_date'] # Default ordering by expiry date

class Profile(models.Model):
    """Extends the default User model to add role information."""

    class Role(models.TextChoices):
        ADMIN = 'ADM', _('Admin')
        VIEWER = 'VWR', _('Viewer')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=3,
        choices=Role.choices,
        default=Role.VIEWER,
        help_text="User role determining permissions"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# Optional: Add a signal to automatically create/update Profile when User is created/updated
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
