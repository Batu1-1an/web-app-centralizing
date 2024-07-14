# IT Asset Manager Web Application

## Overview

This web application provides a centralized system for tracking critical IT assets, focusing on licenses, domains, SSL certificates, and software subscriptions. It aims to prevent service lapses by managing expiry dates and automating renewal alerts.

Built with Python, Django, and PostgreSQL (using Supabase as the backend provider), it offers a user-friendly interface with role-based access control.

## Features

*   **Asset Tracking:** Manage various IT assets (Licenses, Domains, SSL Certificates, Software Subscriptions).
*   **Detailed Information:** Store key details for each asset, including name, type, vendor, expiry date, cost, associated user, and department.
*   **CRUD Operations:** Web interface for Creating, Reading, Updating, and Deleting assets.
*   **Role-Based Access:**
    *   **Admin:** Full CRUD access.
    *   **Viewer:** Read-only access (Note: Currently, all logged-in users can view, but only Admins can modify).
*   **Dashboard:** Provides a summary of total assets and highlights assets nearing expiry (within 30, 60, 90 days).
*   **Renewal Alerts (Command):** Includes a management command (`check_renewals`) to identify assets nearing expiry. (Requires configuration and scheduling to send email notifications).
*   **Modern UI:** Styled using Bootstrap 5 for a responsive and professional look.

## Technology Stack

*   **Backend:** Python 3.11+, Django 5.2+
*   **Database:** PostgreSQL (Designed for Supabase, but adaptable)
*   **Frontend:** Django Templates, HTML, Bootstrap 5, Bootstrap Icons
*   **Database Driver:** `psycopg[binary]`
*   **Testing:** Django Test Framework (`unittest`)

## Project Structure

```
.
├── .git/                 # Git repository data
├── .gitignore            # Specifies intentionally untracked files
├── PLAN.md               # Project development plan
├── assets/               # Core application for asset management
│   ├── __init__.py
│   ├── admin.py          # Django admin configuration
│   ├── apps.py           # App configuration
│   ├── management/       # Custom management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── check_renewals.py # Renewal alert command
│   ├── migrations/       # Database migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── mixins.py         # Custom view mixins (e.g., AdminRequiredMixin)
│   ├── models.py         # Database models (Asset, Profile)
│   ├── templates/        # App-specific templates
│   │   └── assets/
│   │       ├── asset_confirm_delete.html
│   │       ├── asset_detail.html
│   │       ├── asset_form.html
│   │       ├── asset_list.html
│   │       ├── base.html       # Base template for the app
│   │       └── dashboard.html
│   ├── tests/            # Application tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_commands.py
│   │   ├── test_models.py
│   │   └── test_views.py
│   ├── urls.py           # App-specific URL routing
│   └── views.py          # Application views (CRUD, Dashboard)
├── it_asset_manager/     # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py       # Project settings (DB, templates, email, etc.)
│   ├── urls.py           # Main project URL routing
│   └── wsgi.py
├── manage.py             # Django management script
└── templates/            # Project-level templates
    └── registration/     # Templates for django.contrib.auth
        ├── logged_out.html
        └── login.html
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Batu1-1an/web-app-centralizing.git
    cd web-app-centralizing
    ```
2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install django psycopg[binary]
    # Or if a requirements.txt file is created later:
    # pip install -r requirements.txt
    ```
4.  **Configure Database:**
    *   Open `it_asset_manager/settings.py`.
    *   Locate the `DATABASES` dictionary.
    *   Replace the placeholder values for `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT` with your actual PostgreSQL database credentials (e.g., from Supabase).
5.  **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create a Superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.
7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
8.  **Access the Application:** Open your web browser and go to `http://127.0.0.1:8000/`. You should be redirected to the dashboard.
9.  **Access the Admin Panel:** Go to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

## Usage

1.  **Login:** Access the login page at `/accounts/login/`.
2.  **Admin Setup:** Log in to the Django Admin (`/admin/`) as a superuser. Navigate to "Assets" -> "Profiles". Select your user profile and change the "Role" to "Admin". Save the changes.
3.  **Manage Assets:** Log in to the main application (`/accounts/login/`).
    *   **Dashboard (`/assets/dashboard/`):** View asset summary and upcoming renewals.
    *   **Asset List (`/assets/`):** View all tracked assets.
    *   **Add Asset:** Click the "Add New Asset" button (visible to Admins).
    *   **View Details:** Click on an asset's name in the list.
    *   **Edit/Delete:** Use the buttons on the asset detail page (visible to Admins).
4.  **Renewal Alerts:**
    *   **Configure Email:** Update the `EMAIL_*` settings in `it_asset_manager/settings.py` with your email provider's details. Set `EMAIL_BACKEND` to `django.core.mail.backends.smtp.EmailBackend`. Update the `recipient_list` in `assets/management/commands/check_renewals.py`.
    *   **Run Manually:** `python manage.py check_renewals` (use `--dry-run` to test without sending).
    *   **Schedule:** Set up a cron job (Linux/macOS) or Task Scheduler (Windows) to run `python manage.py check_renewals` daily.

## Future Enhancements (Potential)

*   Implement filtering, sorting, and pagination on the Asset List view.
*   Add more detailed permission checks (e.g., allow specific users/groups to manage specific asset types).
*   Improve email notification formatting and recipient logic (e.g., email asset owner).
*   Add file uploads for related documents (invoices, license files).
*   Implement more comprehensive testing (integration tests).
*   Refine UI/UX further.