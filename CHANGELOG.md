# Changelog

All notable changes to the IT Asset Manager project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dockerfile with multi-stage build for production deployment
- docker-compose.yml with PostgreSQL 16 service and health checks
- gunicorn as production WSGI server
- CHANGELOG.md and CONTRIBUTING.md for open-source contributors
- MIT LICENSE file
- `python-dotenv` support in manage.py for automatic `.env` loading
- Production security settings: ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, SECURE_PROXY_SSL_HEADER
- Whitenoise static file serving for production
- STATIC_ROOT configuration for `collectstatic`
- Auto-creation of Profile via post_save signal on User creation
- Dashboard view tests covering totals, upcoming renewals, and expiring assets

### Fixed
- Removed duplicate "Add New Asset" button in asset_list.html
- Settings now read ALLOWED_HOSTS from environment variable instead of empty list

### Changed
- Enhanced .env.example with ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, and security options
- Improved admin.py with list_display, search_fields, and list_filter for Asset and Profile
- Upgraded delete confirmation template with Bootstrap 5 styling

## [0.1.0] - 2025-03-15

### Added
- Multi-type asset tracking (Licenses, Domains, SSL Certificates, Software Subscriptions)
- Full CRUD interface with Bootstrap 5.3 responsive UI
- Role-Based Access Control (Admin / Viewer) with custom mixins
- Expiry dashboard with counts at 30, 60, and 90-day thresholds
- Automated renewal alert management command (`check_renewals`)
- Email notification system with console fallback for development
- Django admin registrations for Asset and Profile models
- Comprehensive test suite: 14+ test cases across models, views, auth, and commands
- PostgreSQL database support (Supabase-ready)
- Project documentation with architecture overview and quick-start guide
