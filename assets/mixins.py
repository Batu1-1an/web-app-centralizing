from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from .models import Profile # Assuming Profile model is in the same app

class AdminRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is an admin."""

    def test_func(self):
        # Check if user is authenticated first (LoginRequiredMixin should handle this, but good practice)
        if not self.request.user.is_authenticated:
            return False
        try:
            # Check if the user has a profile and if their role is Admin
            return self.request.user.profile.role == Profile.Role.ADMIN
        except Profile.DoesNotExist:
            # Handle cases where a profile might not exist for a user (e.g., superuser before profile creation)
            # Or raise ImproperlyConfigured if a profile is strictly required for all users
            return False # Deny access if no profile exists

    def handle_no_permission(self):
        # You can customize the behavior for non-admins, e.g., redirect to a specific page or raise PermissionDenied
        # For now, let's rely on the default behavior of UserPassesTestMixin (usually a 403 Forbidden)
        return super().handle_no_permission()