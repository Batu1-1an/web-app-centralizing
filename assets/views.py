# assets/views.py
import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required # For function-based view protection
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Asset
from .mixins import AdminRequiredMixin
# Create your views here.

class AssetListView(ListView):
    model = Asset
    template_name = 'assets/asset_list.html' # We'll create this template next
    context_object_name = 'assets' # Name to use in the template context

    # We'll add permission checks and potentially filtering later
    # def get_queryset(self):
    #     # Potentially filter based on user role or other criteria
    #     return Asset.objects.all()
class AssetDetailView(DetailView):
    model = Asset
    template_name = 'assets/asset_detail.html' # We'll create this template next
    context_object_name = 'asset' # Name to use in the template context

    # We'll add permission checks later

class AssetCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView): # Add AdminRequiredMixin
    model = Asset
    template_name = 'assets/asset_form.html' # We'll create this template next
    fields = ['name', 'asset_type', 'vendor', 'expiry_date', 'cost', 'associated_user', 'associated_department'] # Fields to include in the form
    success_url = '/assets/' # Redirect to asset list on successful creation (we can use reverse_lazy later)
# AdminRequiredMixin handles permission check


@login_required # Protect this view with login
def dashboard(request):
    """Displays a dashboard with summary information."""
    today = timezone.localdate()
    days_thresholds = [30, 60, 90]
    expiring_counts = {}
    expiring_soon_assets = {} # Store assets for listing

    for days in days_thresholds:
        threshold_date = today + datetime.timedelta(days=days)
        count = Asset.objects.filter(
            expiry_date__gt=today, # Expiring in the future
            expiry_date__lte=threshold_date
        ).count()
        expiring_counts[days] = count

        # Get assets expiring within the smallest threshold for listing
        if days == min(days_thresholds):
             expiring_soon_assets = Asset.objects.filter(
                expiry_date__gt=today,
                expiry_date__lte=threshold_date
            ).order_by('expiry_date')[:10] # Limit to 10 for the dashboard list


    total_assets = Asset.objects.count()

    context = {
        'total_assets': total_assets,
        'expiring_counts': expiring_counts,
        'expiring_soon_assets': expiring_soon_assets,
        'soon_threshold': min(days_thresholds),
    }
    return render(request, 'assets/dashboard.html', context)
    # We'll add Admin role permission checks later

class AssetUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView): # Add AdminRequiredMixin
    model = Asset
    template_name = 'assets/asset_form.html' # Reuse the form template
    fields = ['name', 'asset_type', 'vendor', 'expiry_date', 'cost', 'associated_user', 'associated_department'] # Fields to include in the form
    success_url = '/assets/' # Redirect to asset list on successful update (we can use reverse_lazy later)
# AdminRequiredMixin handles permission check
    # We'll add Admin role permission checks later

class AssetDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView): # Add AdminRequiredMixin
    model = Asset
    template_name = 'assets/asset_confirm_delete.html' # We'll create this template next
    success_url = reverse_lazy('assets:asset_list') # Redirect to asset list after deletion
# AdminRequiredMixin handles permission check
# Other views (Detail, Create, Update, Delete) will be added later
