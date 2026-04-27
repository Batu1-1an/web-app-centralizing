<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 5.2" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap 5.3" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

<h1 align="center">IT Asset Manager</h1>

<p align="center">
  A centralized web application for tracking IT assets — licenses, domains, SSL certificates, and software subscriptions — with expiry monitoring, role-based access control, and automated renewal alerts.
  <br /><br />
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#testing">Testing</a> •
  <a href="#project-structure">Project Structure</a>
</p>

---

## Features

- **IT Asset Tracking** — Manage four asset types: Licenses, Domains, SSL Certificates, and Software Subscriptions.
- **Full CRUD Interface** — Create, read, update, and delete assets through a clean web UI.
- **Role-Based Access Control** — Admin role for full CRUD; Viewer role for read-only access. Protected via Django authentication and custom mixins.
- **Expiry Dashboard** — At-a-glance summary showing total assets and counts of items expiring within 30, 60, and 90 days.
- **Automated Renewal Alerts** — Management command (`check_renewals`) that scans for assets nearing expiry and sends email notifications at configurable thresholds (default: 90, 60, 30 days).
- **Responsive UI** — Bootstrap 5.3 frontend with themed badges, icons, and mobile-friendly navigation.
- **Comprehensive Test Suite** — Unit tests covering models, views, authentication, and the renewal command.

## Tech Stack

| Category      | Technology                                          |
|---------------|-----------------------------------------------------|
| **Backend**   | Python 3.11+, Django 5.2                            |
| **Database**  | PostgreSQL (via `psycopg[binary]`) — Supabase-ready |
| **Frontend**  | Django Templates, HTML5, Bootstrap 5.3, Bootstrap Icons |
| **Auth**      | Django `contrib.auth` with custom `Profile` role model |
| **Testing**   | Django Test Framework (`unittest`)                  |
| **Task Runner** | Custom Django management command (cron/celery-ready) |

## Architecture

```
┌─────────────────────────────────────────────┐
│                User Browser                  │
└─────────────────────┬───────────────────────┘
                      │ HTTP
┌─────────────────────▼───────────────────────┐
│            Django Application                │
│  ┌─────────┐  ┌────────┐  ┌──────────────┐  │
│  │ Views /  │  │  ORM   │  │ Renewal      │  │
│  │Templates │  │ / Auth │  │ Check Command│  │
│  └─────────┘  └────────┘  └──────┬───────┘  │
│                                   │          │
│  ┌────────────────────────────┐   │          │
│  │   Email Sending Module     │◄──┘          │
│  └──────────┬─────────────────┘              │
└─────────────┼───────────────┬────────────────┘
              │               │ SMTP
     ┌────────▼────┐   ┌──────▼──────┐
     │  PostgreSQL │   │ Email/SMTP  │
     │  (Supabase) │   │   Service   │
     └─────────────┘   └─────────────┘
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- PostgreSQL database (local or [Supabase](https://supabase.com))
- pip (Python package manager)
- (Optional) Virtual environment tool (`venv`)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Batu1-1an/web-app-centralizing.git
cd web-app-centralizing

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your database credentials and secret key

# 5. Apply database migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you will be redirected to the dashboard.

## Configuration

All sensitive settings are configured via environment variables. Copy `.env.example` to `.env` and adjust:

```ini
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# PostgreSQL (e.g. Supabase)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=your-project.supabase.co
DB_PORT=5432

# SMTP Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

The application falls back to `django.core.mail.backends.console.EmailBackend` when no SMTP is configured, printing emails to the console during development.

## Usage

### Setting Up Roles

1. Log in to the Django Admin at `/admin/` with your superuser credentials.
2. Navigate to **Assets → Profiles**.
3. Edit your user profile and set the **Role** to `Admin`.
4. Save — now you have full CRUD access through the main app.

### Managing Assets

| Endpoint                  | Action                    | Access   |
|---------------------------|---------------------------|----------|
| `/assets/dashboard/`      | View summary & renewals   | Any user |
| `/assets/`                | List all assets           | Any user |
| `/assets/<id>/`           | View asset details        | Any user |
| `/assets/add/`            | Create a new asset        | Admin    |
| `/assets/<id>/edit/`      | Update an asset           | Admin    |
| `/assets/<id>/delete/`    | Delete an asset           | Admin    |

### Renewal Alerts

Run the renewal check manually:

```bash
# Dry run — see what would be sent without actually emailing
python manage.py check_renewals --dry-run

# Send alerts for assets expiring within default thresholds (90, 60, 30 days)
python manage.py check_renewals

# Custom thresholds
python manage.py check_renewals --days 60 20
```

To automate, schedule the command via cron (Linux/macOS) or Task Scheduler (Windows):

```cron
0 8 * * * cd /path/to/project && /path/to/venv/bin/python manage.py check_renewals
```

## Testing

The project includes 14 test cases across 4 test modules:

```bash
python manage.py test assets
```

| Test Module         | Coverage                                       |
|---------------------|-------------------------------------------------|
| `test_models.py`    | Asset field constraints, Profile defaults/roles |
| `test_views.py`     | Template rendering, CRUD form submission, redirects |
| `test_auth.py`      | Login-required gates, Admin vs. Viewer RBAC     |
| `test_commands.py`  | `check_renewals` — dry-run, default/custom thresholds |

## Project Structure

```
web-app-centralizing/
├── .env.example                # Environment variable template
├── .gitignore
├── manage.py                   # Django CLI entrypoint
├── PLAN.md                     # Development plan & architecture
├── requirements.txt            # Python dependencies
├── templates/                  # Project-level templates
│   └── registration/           # Auth templates (login, logout)
│       ├── login.html
│       └── logged_out.html
├── it_asset_manager/           # Django project configuration
│   ├── asgi.py                 # ASGI application
│   ├── wsgi.py                 # WSGI application
│   ├── settings.py             # Settings (DB, email, auth, etc.)
│   └── urls.py                 # Root URL configuration
└── assets/                     # Core application
    ├── admin.py                # Django admin registrations
    ├── apps.py                 # App config
    ├── mixins.py               # AdminRequiredMixin (RBAC)
    ├── models.py               # Asset & Profile models
    ├── urls.py                 # App URL routing
    ├── views.py                # CRUD views + dashboard
    ├── management/
    │   └── commands/
    │       └── check_renewals.py   # Renewal alert command
    ├── migrations/
    │   └── 0001_initial.py
    ├── templates/
    │   └── assets/
    │       ├── base.html           # Base layout (Bootstrap 5.3)
    │       ├── dashboard.html      # Expiry summary view
    │       ├── asset_list.html     # Asset table
    │       ├── asset_detail.html   # Single asset details
    │       ├── asset_form.html     # Create/Edit form
    │       └── asset_confirm_delete.html
    └── tests/
        ├── test_models.py
        ├── test_views.py
        ├── test_auth.py
        └── test_commands.py
```

## Planned Enhancements

- Filtering, sorting, and pagination on the asset list view
- Granular permissions (e.g., per-asset-type access)
- File uploads for invoices and license documents
- Improved email notification formatting and per-owner routing
- Integration/end-to-end tests with `LiveServerTestCase`

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details (if absent, the project is distributed without a license by default).
