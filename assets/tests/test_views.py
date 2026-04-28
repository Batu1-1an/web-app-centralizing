import datetime
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from ..models import Asset, Profile # Use relative import

User = get_user_model()

class AssetViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase."""
        # Create users
        cls.viewer_user = User.objects.create_user(username='viewtester', password='password')
        Profile.objects.create(user=cls.viewer_user, role=Profile.Role.VIEWER)

        cls.admin_user = User.objects.create_user(username='admintester', password='password')
        Profile.objects.create(user=cls.admin_user, role=Profile.Role.ADMIN)

        # Create assets
        cls.asset1 = Asset.objects.create(
            name="View Test Asset 1",
            asset_type=Asset.AssetType.LICENSE,
            expiry_date=timezone.localdate() + datetime.timedelta(days=50)
        )
        cls.asset2 = Asset.objects.create(
            name="View Test Asset 2",
            asset_type=Asset.AssetType.DOMAIN,
            expiry_date=timezone.localdate() + datetime.timedelta(days=100)
        )

        # URLs
        cls.list_url = reverse('assets:asset_list')
        cls.detail_url_1 = reverse('assets:asset_detail', args=[cls.asset1.pk])
        cls.add_url = reverse('assets:asset_add')
        cls.edit_url_1 = reverse('assets:asset_edit', args=[cls.asset1.pk])
        cls.delete_url_1 = reverse('assets:asset_delete', args=[cls.asset1.pk])
        cls.dashboard_url = reverse('assets:dashboard')

        # Client
        cls.client = Client()

    # --- List View Tests ---
    def test_list_view_uses_correct_template(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets/asset_list.html')
        self.assertTemplateUsed(response, 'assets/base.html')

    def test_list_view_displays_assets(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.asset1.name)
        self.assertContains(response, self.asset2.name)
        self.assertIn('assets', response.context)
        self.assertEqual(len(response.context['assets']), 2)

    # --- Detail View Tests ---
    def test_detail_view_uses_correct_template(self):
        response = self.client.get(self.detail_url_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets/asset_detail.html')
        self.assertTemplateUsed(response, 'assets/base.html')

    def test_detail_view_displays_correct_asset(self):
        response = self.client.get(self.detail_url_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.asset1.name)
        self.assertNotContains(response, self.asset2.name)
        self.assertIn('asset', response.context)
        self.assertEqual(response.context['asset'], self.asset1)

    # --- Create View Tests (Initial GET) ---
    def test_create_view_get_request_as_admin(self):
        """Test GET request for create view as admin."""
        self.client.login(username='admintester', password='password')
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets/asset_form.html')
        self.assertIn('form', response.context)
        self.client.logout()

    # --- Update View Tests (Initial GET) ---
    def test_update_view_get_request_as_admin(self):
        """Test GET request for update view as admin."""
        self.client.login(username='admintester', password='password')
        response = self.client.get(self.edit_url_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets/asset_form.html')
        self.assertIn('form', response.context)
        # Check if form is pre-filled (form instance should be the asset)
        self.assertEqual(response.context['form'].instance, self.asset1)
        self.client.logout()

    # --- Delete View Tests (Initial GET) ---
    def test_delete_view_get_request_as_admin(self):
        """Test GET request for delete view as admin."""
        self.client.login(username='admintester', password='password')
        response = self.client.get(self.delete_url_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets/asset_confirm_delete.html')
        self.assertIn('object', response.context) # Default context name for DeleteView
        self.assertEqual(response.context['object'], self.asset1)
        self.client.logout()

    # --- Create View Tests (POST) ---
    def test_create_view_post_request_as_admin(self):
        """Test POST request for create view as admin."""
        self.client.login(username='admintester', password='password')
        initial_count = Asset.objects.count()
        post_data = {
            'name': 'New Asset via Test',
            'asset_type': Asset.AssetType.SSL_CERTIFICATE,
            'expiry_date': (timezone.localdate() + datetime.timedelta(days=365)).strftime('%Y-%m-%d'),
            'vendor': 'Test Cert Inc.',
            # Add other required fields if any, or ensure they allow blank/null
            'cost': '', # Optional field
            'associated_user': '', # Optional field
            'associated_department': 'Test Dept', # Optional field
        }
        response = self.client.post(self.add_url, data=post_data)

        # Should redirect to list view on success
        self.assertRedirects(response, self.list_url)
        # Check if asset count increased
        self.assertEqual(Asset.objects.count(), initial_count + 1)
        # Check if the new asset exists and has correct data
        new_asset = Asset.objects.get(name='New Asset via Test')
        self.assertEqual(new_asset.asset_type, Asset.AssetType.SSL_CERTIFICATE)
        self.assertEqual(new_asset.vendor, 'Test Cert Inc.')
        self.assertEqual(new_asset.associated_department, 'Test Dept')
        self.client.logout()

    # --- Update View Tests (POST) ---
    def test_update_view_post_request_as_admin(self):
        """Test POST request for update view as admin."""
        self.client.login(username='admintester', password='password')
        updated_name = "UPDATED Asset Name"
        post_data = {
            'name': updated_name,
            'asset_type': self.asset1.asset_type, # Keep original type
            'expiry_date': self.asset1.expiry_date.strftime('%Y-%m-%d'), # Keep original date
            'vendor': 'Updated Vendor Co.',
            # Include all fields required by the form, even if empty for optional
            'cost': '',
            'associated_user': '',
            'associated_department': 'Updated Dept',
        }
        response = self.client.post(self.edit_url_1, data=post_data)

        # Should redirect to list view on success
        self.assertRedirects(response, self.list_url)
        # Refresh the asset from DB and check if updated
        self.asset1.refresh_from_db()
        self.assertEqual(self.asset1.name, updated_name)
        self.assertEqual(self.asset1.vendor, 'Updated Vendor Co.')
        self.assertEqual(self.asset1.associated_department, 'Updated Dept')
        self.client.logout()

    # --- Delete View Tests (POST) ---
    def test_delete_view_post_request_as_admin(self):
        """Test POST request for delete view as admin."""
        self.client.login(username='admintester', password='password')
        # Create a new asset specifically for this delete test
        asset_to_delete = Asset.objects.create(
            name="Asset To Delete",
            asset_type=Asset.AssetType.LICENSE,
            expiry_date=timezone.localdate() + datetime.timedelta(days=10)
        )
        delete_url = reverse('assets:asset_delete', args=[asset_to_delete.pk])
        initial_count = Asset.objects.count()

        response = self.client.post(delete_url) # POST confirms deletion

        # Should redirect to list view on success
        self.assertRedirects(response, self.list_url)
        # Check if asset count decreased
        self.assertEqual(Asset.objects.count(), initial_count - 1)
        # Check if the asset no longer exists
        with self.assertRaises(Asset.DoesNotExist):
            Asset.objects.get(pk=asset_to_delete.pk)
        self.client.logout()

    # --- Dashboard View Tests ---
    def test_dashboard_view_uses_correct_template(self):
        """Test dashboard renders the correct template."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets/dashboard.html')
        self.assertTemplateUsed(response, 'assets/base.html')

    def test_dashboard_view_shows_total_assets(self):
        """Test dashboard displays total asset count."""
        response = self.client.get(self.dashboard_url)
        self.assertIn('total_assets', response.context)
        self.assertEqual(response.context['total_assets'], 2)

    def test_dashboard_view_shows_expiring_counts(self):
        """Test dashboard displays expiring counts per threshold."""
        response = self.client.get(self.dashboard_url)
        self.assertIn('expiring_counts', response.context)
        counts = response.context['expiring_counts']
        self.assertIn(30, counts)
        self.assertIn(60, counts)
        self.assertIn(90, counts)
        self.assertEqual(counts[30], 0)  # asset1 expires in 50d, not within 30
        self.assertEqual(counts[60], 1)  # asset1 expires in 50d, within 60
        self.assertEqual(counts[90], 0)  # asset2 expires in 100d, not within 90

    def test_dashboard_view_context_keys(self):
        """Test dashboard provides all expected context keys."""
        response = self.client.get(self.dashboard_url)
        expected_keys = ['total_assets', 'expiring_counts', 'expiring_soon_assets', 'soon_threshold']
        for key in expected_keys:
            self.assertIn(key, response.context)

    def test_dashboard_view_shows_soon_threshold(self):
        """Test dashboard soon_threshold is the minimum threshold."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context['soon_threshold'], 30)