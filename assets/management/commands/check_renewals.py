import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from assets.models import Asset

class Command(BaseCommand):
    help = 'Checks for assets nearing expiry and sends renewal notification emails.'

    def add_arguments(self, parser):
        # Optional: Add arguments, e.g., to specify notification days or dry run
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate sending emails without actually sending them.',
        )
        parser.add_argument(
            '--days',
            nargs='+',
            type=int,
            default=[90, 60, 30],
            help='List of days before expiry to check for (e.g., --days 90 60 30).',
        )

    def handle(self, *args, **options):
        today = timezone.localdate() # Use timezone-aware date
        dry_run = options['dry_run']
        notification_days = sorted(list(set(options['days'])), reverse=True) # Ensure unique and sorted days

        if not notification_days:
            self.stdout.write(self.style.WARNING('No notification days specified. Exiting.'))
            return

        self.stdout.write(f"Checking for assets expiring within {', '.join(map(str, notification_days))} days...")

        expiring_assets = {} # Dictionary to hold assets for each notification threshold

        for days in notification_days:
            expiry_date_threshold = today + datetime.timedelta(days=days)
            # Find assets expiring exactly 'days' from now
            # We might need a more robust way to track *which* notification was sent
            # For now, let's find assets expiring ON or BEFORE the threshold date
            # but AFTER the next threshold (to avoid duplicates in this run)
            # A better approach might involve a 'last_notified_level' field on the Asset model.

            # Simple approach: Find assets expiring between (today + lower_threshold) and (today + days)
            lower_bound_days = 0
            for lower_days in sorted(notification_days, reverse=False):
                 if lower_days < days:
                     lower_bound_days = lower_days
                 else:
                     break # Found the next lower threshold

            lower_date_threshold = today + datetime.timedelta(days=lower_bound_days)

            assets_in_window = Asset.objects.filter(
                expiry_date__gt=lower_date_threshold, # Expiring after the previous threshold (or today if none)
                expiry_date__lte=expiry_date_threshold # Expiring on or before this threshold
            )

            if assets_in_window.exists():
                expiring_assets[days] = assets_in_window
                self.stdout.write(f"Found {assets_in_window.count()} assets expiring in the next {lower_bound_days}-{days} days.")


        if not expiring_assets:
            self.stdout.write(self.style.SUCCESS('No assets require renewal notifications today.'))
            return

        # --- Email Sending Logic ---
        # Improve this: Group emails or send one summary email? Send to asset owner? Admin?
        # For now, send one email per asset to a default admin/recipient list

        # Define recipients (replace with actual admin emails or a setting)
        recipient_list = ['admin@example.com'] # TODO: Make this configurable

        email_count = 0
        for days, assets in expiring_assets.items():
            for asset in assets:
                subject = f"Renewal Alert: Asset '{asset.name}' expiring in {days} days!"
                message = (
                    f"The following asset is nearing its expiry date:\n\n"
                    f"Name: {asset.name}\n"
                    f"Type: {asset.get_asset_type_display()}\n"
                    f"Vendor: {asset.vendor or 'N/A'}\n"
                    f"Expiry Date: {asset.expiry_date.strftime('%Y-%m-%d')}\n"
                    f"Associated User: {asset.associated_user.username if asset.associated_user else 'N/A'}\n"
                    f"Department: {asset.associated_department or 'N/A'}\n\n"
                    f"Please take action to renew this asset soon.\n\n"
                    f"Notification triggered for the {days}-day threshold."
                )
                from_email = settings.DEFAULT_FROM_EMAIL

                if dry_run:
                    self.stdout.write(f"\n--- DRY RUN: Would send email ---")
                    self.stdout.write(f"To: {', '.join(recipient_list)}")
                    self.stdout.write(f"From: {from_email}")
                    self.stdout.write(f"Subject: {subject}")
                    self.stdout.write(f"Message:\n{message}")
                    self.stdout.write(f"---------------------------------")
                    email_count += 1
                else:
                    try:
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                        self.stdout.write(self.style.SUCCESS(f"Sent notification for '{asset.name}' ({days} days)."))
                        email_count += 1
                        # TODO: Add logic here to mark that this notification level was sent for this asset
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Failed to send email for '{asset.name}': {e}"))

        self.stdout.write(f"\nFinished checking renewals. {'Would have sent' if dry_run else 'Sent'} {email_count} notification(s).")