# assets/urls.py
from django.urls import path
from . import views # Import views

app_name = 'assets' # Namespace for URLs

urlpatterns = [
    # Map the root of the app to the AssetListView
    path('', views.AssetListView.as_view(), name='asset_list'),
    # Map URLs like /assets/1/ to the AssetDetailView
    path('<int:pk>/', views.AssetDetailView.as_view(), name='asset_detail'),
    # Map URLs like /assets/add/ to the AssetCreateView
    path('add/', views.AssetCreateView.as_view(), name='asset_add'),
    # Map URLs like /assets/1/edit/ to the AssetUpdateView
    path('<int:pk>/edit/', views.AssetUpdateView.as_view(), name='asset_edit'),
    # Map URLs like /assets/1/delete/ to the AssetDeleteView
    path('<int:pk>/delete/', views.AssetDeleteView.as_view(), name='asset_delete'),
    # Map /assets/dashboard/ to the dashboard view
    path('dashboard/', views.dashboard, name='dashboard'),
]