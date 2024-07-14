import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Asset, Profile # Use relative import within the package

User = get_user_model()

class AssetModelTests(TestCase):

    def setUp(self):
        """Set up a test user for foreign key relations if needed."""
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_asset_creation(self):
        """Test creating an Asset instance."""
        now = timezone.localdate()
        expiry = now + datetime.timedelta(days=30)
        asset = Asset.objects.create(
            name="Test License",
            asset_type=Asset.AssetType.LICENSE,
            vendor="Test Vendor",
            expiry_date=expiry,
            cost=99.99,
            associated_user=self.user,
            associated_department="IT"
        )
        self.assertEqual(asset.name, "Test License")
        self.assertEqual(asset.asset_type, Asset.AssetType.LICENSE)
        self.assertEqual(asset.vendor, "Test Vendor")
        self.assertEqual(asset.expiry_date, expiry)
        self.assertEqual(asset.cost, 99.99)
        self.assertEqual(asset.associated_user, self.user)
        self.assertEqual(asset.associated_department, "IT")
        self.assertEqual(str(asset), f"License: Test License")
        self.assertTrue(isinstance(asset.created_at, datetime.datetime))
        self.assertTrue(isinstance(asset.updated_at, datetime.datetime))

class ProfileModelTests(TestCase):

    def setUp(self):
        """Set up a test user."""
        self.user = User.objects.create_user(username='testprofileuser', password='password')
        # Manually create profile as we didn't implement the signal
        self.profile = Profile.objects.create(user=self.user)


    def test_profile_creation_and_defaults(self):
        """Test that a profile is linked and has the default role."""
        self.assertEqual(self.profile.user, self.user)
        # Check default role
        self.assertEqual(self.profile.role, Profile.Role.VIEWER)
        self.assertEqual(str(self.profile), f"testprofileuser - Viewer")

    def test_profile_role_change(self):
        """Test changing the role of a profile."""
        self.profile.role = Profile.Role.ADMIN
        self.profile.save()
        # Re-fetch from DB to be sure
        updated_profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(updated_profile.role, Profile.Role.ADMIN)
        self.assertEqual(str(updated_profile), f"testprofileuser - Admin")