<div align="center">

# IT Asset Manager

**Centralized lifecycle tracking for licenses, domains, SSL certificates, and software subscriptions — with expiry monitoring, RBAC, and automated renewal alerts.**


![Python 3.11+](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django 5.2](https://img.shields.io/badge/Django_5.2-092E20?style=flat-square&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Bootstrap 5.3](https://img.shields.io/badge/Bootstrap_5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)
![Supabase Ready](https://img.shields.io/badge/Supabase_Ready-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![License MIT](https://img.shields.io/badge/License_MIT-6B9F00?style=flat-square)

---

[Features](#features) •
[Why This App?](#why-this-app) •
[Architecture](#architecture) •
[Screenshots](#screenshots) •
[Quick Start](#quick-start) •
[Configuration](#configuration) •
[Usage](#usage) •
[Testing](#testing) •
[Project Structure](#project-structure) •
[Planned Enhancements](#planned-enhancements)

</div>

## Why This App?

IT assets are the backbone of every organization, yet they're often scattered across spreadsheets, sticky notes, and inboxes. Licenses expire without warning. Domains lapse. SSL certificates go unnoticed until the browser screams **"Not Secure."**

**IT Asset Manager** consolidates everything into one place: track what you own, know what's expiring, and automate renewals — so you can stop firefighting and start managing.

## Features

| Icon | Feature | Description |
|------|---------|-------------|
| 📦 | **Multi-Type Asset Tracking** | Manage Licenses, Domains, SSL Certificates, and Software Subscriptions from a single interface. |
| ✏️ | **Full CRUD Interface** | Create, read, update, and delete assets through a clean, responsive web UI. |
| 🔐 | **Role-Based Access Control** | Admin role for full CRUD; Viewer role for read-only access — enforced via Django authentication and custom mixins. |
| 📊 | **Expiry Dashboard** | At-a-glance summary showing total asset counts and items expiring within 30, 60, and 90 days. |
| 📬 | **Automated Renewal Alerts** | Built-in `check_renewals` management command scans for expiring assets and sends email notifications at configurable thresholds (defaults: 90, 60, 30 days). |
| 📱 | **Responsive UI** | Bootstrap 5.3 interface with themed badges, icons, and mobile-friendly navigation. |
| ✅ | **Comprehensive Test Suite** | Unit tests covering models, views, authentication, and the renewal command — 14 test cases across 4 modules. |

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    User Browser                        │
│           (Django Templates + Bootstrap 5.3)           │
└────────────────────────┬─────────────────────────────┘
                         │ HTTP / HTTPS
                         ▼
┌──────────────────────────────────────────────────────┐
│                Django Application                      │
│                                                        │
│  ┌─────────────────┐  ┌──────────────┐               │
│  │   Views /        │  │     ORM      │               │
│  │   Templates      │  │   / Auth     │               │
│  │                  │  │              │               │
│  │  • Dashboard     │  │  • Asset     │               │
│  │  • Asset CRUD    │  │  • Profile   │               │
│  │  • Auth Pages    │  │  • Perms     │               │
│  └────────┬────────┘  └──────┬───────┘               │
│           │                  │                         │
│  ┌────────▼──────────────────▼───────────────────┐   │
│  │           Renewal Check Command                │   │
│  │    python manage.py check_renewals [--dry-run] │   │
│  └────────────────────┬──────────────────────────┘   │
│                       │                                │
│  ┌────────────────────▼──────────────────────────┐   │
│  │           Email Sending Module                  │   │
│  │   SMTP │ ConsoleBackend (dev fallback)          │   │
│  └────────────────────┬──────────────────────────┘   │
└───────────────────────┼──────────────────────────────┘
                        │
              ┌─────────▼──────────┬──────────────────┐
              │     PostgreSQL      │   Email / SMTP    │
              │  (Supabase Ready)   │     Service       │
              └────────────────────┘──────────────────┘
```

## Screenshots

<div align="center">
  <table>
    <tr>
      <td align="center"><b>Dashboard</b></td>
      <td align="center"><b>Asset List</b></td>
      <td align="center"><b>Asset Detail</b></td>
    </tr>
    <tr>
      <td>
        <div style="border:1px solid #e0e0e0; border-radius:8px; padding:40px 20px; text-align:center; background:#f9fafb; min-width:240px;">
          <span style="font-size:2.5rem;">📊</span>
          <p style="color:#666; margin-top:8px;">Expiry summary, counts by threshold, quick navigation</p>
        </div>
      </td>
      <td>
        <div style="border:1px solid #e0e0e0; border-radius:8px; padding:40px 20px; text-align:center; background:#f9fafb; min-width:240px;">
          <span style="font-size:2.5rem;">📋</span>
          <p style="color:#666; margin-top:8px;">Filterable table of all assets with status badges</p>
        </div>
      </td>
      <td>
        <div style="border:1px solid #e0e0e0; border-radius:8px; padding:40px 20px; text-align:center; background:#f9fafb; min-width:240px;">
          <span style="font-size:2.5rem;">🔍</span>
          <p style="color:#666; margin-top:8px;">Full asset metadata, edit/delete actions</p>
        </div>
      </td>
    </tr>
  </table>
</div>

## Quick Start

### Prerequisites

- Python **3.11+**
- PostgreSQL database (local or [Supabase](https://supabase.com))
- `pip` + `venv` (or your preferred environment manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Batu1-1an/web-app-centralizing.git
cd web-app-centralizing

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env        # then edit .env with your credentials

# Run database migrations
python manage.py migrate

# Create an admin superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser — you'll be redirected to the dashboard.

## Configuration

All sensitive settings are configured via environment variables. Copy `.env.example` to `.env` and populate:

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | `django-insecure-...` | Django secret key (**change in production**) |
| `DJANGO_DEBUG` | `False` | Enable debug mode (`True` / `False`) |
| `DB_ENGINE` | `django.db.backends.postgresql` | Database engine |
| `DB_NAME` | `postgres` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | *(empty)* | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `EMAIL_BACKEND` | `console.EmailBackend` | Email backend class |
| `EMAIL_HOST` | `smtp.example.com` | SMTP server host |
| `EMAIL_PORT` | `587` | SMTP server port |
| `EMAIL_USE_TLS` | `True` | Enable TLS for SMTP |
| `EMAIL_HOST_USER` | *(empty)* | SMTP username |
| `EMAIL_HOST_PASSWORD` | *(empty)* | SMTP password |
| `DEFAULT_FROM_EMAIL` | `noreply@example.com` | Default sender address |

> When SMTP is unconfigured, the app falls back to `django.core.mail.backends.console.EmailBackend`, printing emails to the console — perfect for local development.

## Usage

### Setting Up Roles

1. Log in to Django Admin at **`/admin/`** with your superuser account.
2. Navigate to **Assets → Profiles**.
3. Edit your profile and set the **Role** field to `Admin`.
4. Save — you now have full CRUD access throughout the app.

### Managing Assets

| Endpoint | Action | Access |
|----------|--------|--------|
| `/assets/dashboard/` | View expiry summary & counts | Any authenticated user |
| `/assets/` | List all assets | Any authenticated user |
| `/assets/<id>/` | View asset detail | Any authenticated user |
| `/assets/add/` | Create a new asset | Admin only |
| `/assets/<id>/edit/` | Update an asset | Admin only |
| `/assets/<id>/delete/` | Delete an asset | Admin only |

### Renewal Alerts

```bash
# Dry run — preview alerts without sending emails
python manage.py check_renewals --dry-run

# Send alerts for assets expiring within default thresholds (90, 60, 30 days)
python manage.py check_renewals

# Custom thresholds (e.g., 60 and 20 days)
python manage.py check_renewals --days 60 20
```

#### Automate via Cron

Add this line to your crontab to run daily at 8:00 AM:

```cron
0 8 * * * cd /path/to/web-app-centralizing && /path/to/venv/bin/python manage.py check_renewals
```

On Windows, use Task Scheduler to trigger the same command.

## Testing

```bash
python manage.py test assets
```

| Module | Tests | Coverage |
|--------|-------|----------|
| `test_models.py` | 3 | Asset field constraints, Profile defaults & roles |
| `test_views.py` | 4 | Template rendering, CRUD form submission, redirects |
| `test_auth.py` | 4 | Login-required gates, Admin vs. Viewer RBAC enforcement |
| `test_commands.py` | 3 | `check_renewals` dry-run, default + custom thresholds |
| **Total** | **14** | **Core application logic** |

## Project Structure

```
web-app-centralizing/
├── .env.example                    # Environment variable template
├── .gitignore
├── manage.py                       # Django CLI entry point
├── requirements.txt                # Python dependencies
├── templates/                      # Project-level templates
│   └── registration/               # Auth templates (login, logout)
│       ├── login.html
│       └── logged_out.html
├── it_asset_manager/               # Django project configuration
│   ├── asgi.py                     # ASGI application entry point
│   ├── wsgi.py                     # WSGI application entry point
│   ├── settings.py                 # Settings (DB, email, auth, static files)
│   └── urls.py                     # Root URL configuration
├── assets/                         # Core IT asset management app
│   ├── admin.py                    # Django admin registrations
│   ├── apps.py                     # Application configuration
│   ├── mixins.py                   # AdminRequiredMixin (RBAC enforcement)
│   ├── models.py                   # Asset & Profile models
│   ├── urls.py                     # App-level URL routing
│   ├── views.py                    # CRUD views + dashboard
│   ├── management/                 # Custom management commands
│   │   └── commands/
│   │       └── check_renewals.py   # Renewal alert automation
│   ├── migrations/
│   │   └── 0001_initial.py         # Initial database schema
│   ├── templates/
│   │   └── assets/                 # App templates (Bootstrap 5.3)
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── asset_list.html
│   │       ├── asset_detail.html
│   │       ├── asset_form.html
│   │       └── asset_confirm_delete.html
│   └── tests/                      # Test suite
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_views.py
│       ├── test_auth.py
│       └── test_commands.py
└── docs/
    └── PLAN.md                     # Development plan & architecture notes
```

## Planned Enhancements

- 🔍 **Filtering, sorting & pagination** on the asset list view
- 🛡️ **Granular permissions** — per-asset-type access control
- 📎 **File uploads** — attach invoices, license PDFs, and certificates
- 📧 **Rich email notifications** — HTML templates, per-owner routing
- 🧪 **End-to-end tests** using Django's `LiveServerTestCase`
- 🔌 **REST API** — expose assets via DRF for external integrations
- 🐳 **Docker Compose** — one-command local environment setup

## License

<div align="center">

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

Built with [Django](https://www.djangoproject.com/) · [Bootstrap](https://getbootstrap.com/) · [Supabase](https://supabase.com)

</div>
