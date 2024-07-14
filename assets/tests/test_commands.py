import datetime
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from ..models import Asset # Use relative import

class CheckRenewalsCommandTests(TestCase):

    def setUp(self):
        """Set up assets with various expiry dates."""
        self.today = timezone.localdate() # Keep track of the real 'today' for relative dates

        # Asset expiring in 25 days (should trigger 30-day alert)
        Asset.objects.create(
            name="Expires in 25d",
            asset_type=Asset.AssetType.LICENSE,
            expiry_date=self.today + datetime.timedelta(days=25)
        )
        # Asset expiring in 55 days (should trigger 60-day alert)
        Asset.objects.create(
            name="Expires in 55d",
            asset_type=Asset.AssetType.DOMAIN,
            expiry_date=self.today + datetime.timedelta(days=55)
        )
        # Asset expiring in 85 days (should trigger 90-day alert)
        Asset.objects.create(
            name="Expires in 85d",
            asset_type=Asset.AssetType.SSL_CERTIFICATE,
            expiry_date=self.today + datetime.timedelta(days=85)
        )
        # Asset expiring in 100 days (should not trigger default alerts)
        Asset.objects.create(
            name="Expires in 100d",
            asset_type=Asset.AssetType.SOFTWARE_SUBSCRIPTION,
            expiry_date=self.today + datetime.timedelta(days=100)
        )
        # Asset already expired (should not trigger alerts)
        Asset.objects.create(
            name="Expired Asset",
            asset_type=Asset.AssetType.LICENSE,
            expiry_date=self.today - datetime.timedelta(days=10)
        )

    @patch('django.utils.timezone.localdate') # Mock today's date
    def test_check_renewals_dry_run_default_days(self, mock_localdate):
        """Test the command with --dry-run and default days."""
        # Set the mocked date to be the same as our setUp 'today'
        mock_localdate.return_value = self.today
        out = StringIO() # Capture stdout
        call_command('check_renewals', '--dry-run', stdout=out)
        output = out.getvalue()

        # Check output for expected messages
        self.assertIn("Checking for assets expiring within 90, 60, 30 days...", output)
        self.assertIn("Found 1 assets expiring in the next 0-30 days.", output)
        self.assertIn("Found 1 assets expiring in the next 30-60 days.", output)
        self.assertIn("Found 1 assets expiring in the next 60-90 days.", output)

        # Check dry run output for specific assets
        self.assertIn("DRY RUN: Would send email", output)
        self.assertIn("Subject: Renewal Alert: Asset 'Expires in 25d' expiring in 30 days!", output)
        self.assertIn("Subject: Renewal Alert: Asset 'Expires in 55d' expiring in 60 days!", output)
        self.assertIn("Subject: Renewal Alert: Asset 'Expires in 85d' expiring in 90 days!", output)
        self.assertNotIn("Expires in 100d", output) # Should not be included
        self.assertNotIn("Expired Asset", output) # Should not be included

        self.assertIn("Finished checking renewals. Would have sent 3 notification(s).", output)

    @patch('django.utils.timezone.localdate') # Mock today's date
    def test_check_renewals_dry_run_custom_days(self, mock_localdate):
        """Test the command with --dry-run and custom --days argument."""
        mock_localdate.return_value = self.today
        out = StringIO()
        call_command('check_renewals', '--dry-run', '--days', '60', '20', stdout=out) # Custom days
        output = out.getvalue()

        self.assertIn("Checking for assets expiring within 60, 20 days...", output)
        self.assertNotIn("Found 1 assets expiring in the next 0-30 days.", output) # 30 day threshold not used
        self.assertNotIn("Found 1 assets expiring in the next 60-90 days.", output) # 90 day threshold not used
        self.assertIn("Found 0 assets expiring in the next 0-20 days.", output) # Asset at 25d is outside this
        self.assertIn("Found 1 assets expiring in the next 20-60 days.", output) # Asset at 55d is inside this

        self.assertIn("Subject: Renewal Alert: Asset 'Expires in 55d' expiring in 60 days!", output)
        self.assertNotIn("Expires in 25d", output)
        self.assertNotIn("Expires in 85d", output)

        self.assertIn("Finished checking renewals. Would have sent 1 notification(s).", output)

    # Note: Testing actual email sending requires mocking send_mail or using mail.outbox
    # and configuring email settings properly, which is more involved.
    # These dry-run tests cover the core logic of identifying assets.