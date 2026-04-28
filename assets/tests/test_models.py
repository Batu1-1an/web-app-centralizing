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

    def test_asset_without_optional_fields(self):
        """Test creating an Asset with only required fields."""
        now = timezone.localdate()
        expiry = now + datetime.timedelta(days=30)
        asset = Asset.objects.create(
            name="Minimal Asset",
            asset_type=Asset.AssetType.DOMAIN,
            expiry_date=expiry,
        )
        self.assertEqual(asset.name, "Minimal Asset")
        self.assertEqual(asset.vendor, "")
        self.assertIsNone(asset.cost)
        self.assertIsNone(asset.associated_user)
        self.assertEqual(asset.associated_department, "")
        self.assertEqual(str(asset), "Domain: Minimal Asset")

    def test_asset_ordering_by_expiry(self):
        """Test that assets are ordered by expiry_date ascending by default."""
        today = timezone.localdate()
        asset_a = Asset.objects.create(name="Z Later", asset_type=Asset.AssetType.LICENSE, expiry_date=today + datetime.timedelta(days=90))
        asset_b = Asset.objects.create(name="A Sooner", asset_type=Asset.AssetType.LICENSE, expiry_date=today + datetime.timedelta(days=10))
        assets = Asset.objects.all()
        self.assertEqual(assets[0], asset_b)
        self.assertEqual(assets[len(assets) - 1], asset_a)

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

    def test_profile_auto_created_on_user_creation(self):
        """Test that creating a User automatically creates a Profile via signal."""
        new_user = User.objects.create_user(username='autoprofile', password='password')
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertEqual(new_user.profile.role, Profile.Role.VIEWER)