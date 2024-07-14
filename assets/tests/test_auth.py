import datetime
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from assets.models import Asset, Profile

User = get_user_model()

class AuthAccessTests(TestCase):

    def setUp(self):
        """Set up users with different roles and a test asset."""
        self.client = Client()

        # Create Viewer User
        self.viewer_user = User.objects.create_user(username='viewer', password='password')
        Profile.objects.create(user=self.viewer_user, role=Profile.Role.VIEWER)

        # Create Admin User
        self.admin_user = User.objects.create_user(username='admin', password='password')
        Profile.objects.create(user=self.admin_user, role=Profile.Role.ADMIN)

        # Create a test asset
        self.asset = Asset.objects.create(
            name="Test Asset for Auth",
            asset_type=Asset.AssetType.DOMAIN,
            expiry_date=timezone.localdate() + datetime.timedelta(days=10)
        )

        # URLs to test (using reverse for robustness)
        self.list_url = reverse('assets:asset_list')
        self.detail_url = reverse('assets:asset_detail', args=[self.asset.pk])
        self.add_url = reverse('assets:asset_add')
        self.edit_url = reverse('assets:asset_edit', args=[self.asset.pk])
        self.delete_url = reverse('assets:asset_delete', args=[self.asset.pk])
        self.dashboard_url = reverse('assets:dashboard')
        self.login_url = reverse('login') # Default Django login URL name

    def test_logged_out_access(self):
        """Test access for logged-out users."""
        # Publicly accessible views (should be OK)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

        # Protected views (should redirect to login)
        response = self.client.get(self.add_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.add_url}')
        response = self.client.get(self.edit_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.edit_url}')
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.delete_url}')
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.dashboard_url}')


    def test_viewer_access(self):
        """Test access for logged-in users with 'Viewer' role."""
        self.client.login(username='viewer', password='password')

        # Views accessible to viewers
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)

        # Views restricted to Admins (should return 403 Forbidden)
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 403)
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 403)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)

        self.client.logout()

    def test_admin_access(self):
        """Test access for logged-in users with 'Admin' role."""
        self.client.login(username='admin', password='password')

        # All views should be accessible to Admins
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()