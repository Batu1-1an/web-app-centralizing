# IT Asset Management Web Application Plan (with Integrated Testing)

**Project Goal:** Develop a web application using Python/Django and Supabase to centralize the tracking of IT assets (Licenses, Domains, SSL Certificates, Software Subscriptions), manage their details (Name, Vendor, Expiry Date, Cost, User/Department), provide role-based access (Admin, Viewer), automate email renewal alerts (90, 60, 30 days prior), and ensure quality through integrated testing.

**Phase 1: Foundation & Core Models**

1.  **Project Setup:**
    *   Initialize Django project (`it_asset_manager`).
    *   Create `assets` app.
    *   Configure `settings.py` (DB, static, templates, `assets` app).
2.  **Data Modeling (`assets/models.py`):**
    *   Define `Department` model (optional).
    *   Define `Asset` model (fields: name, asset_type, vendor, expiry_date, cost, associated_user, associated_department, created_at, updated_at).
    *   Define `Profile` model (linked to `User`, with `role` field: 'Admin', 'Viewer').
3.  **Admin Interface (`assets/admin.py`):**
    *   Register models with Django admin.
4.  **Migrations:**
    *   Create (`makemigrations`) and apply (`migrate`) initial migrations.
5.  **Testing (Phase 1):**
    *   **Model Tests (`assets/tests/test_models.py`):** Write unit tests to verify model field constraints, default values, and any custom methods on `Asset`, `Department`, and `Profile`.
    *   **Admin Tests:** Basic checks to ensure models are registered and accessible in the admin interface (can be manual initially or using Django's test client).

**Phase 2: User Interface & CRUD Operations**

1.  **Authentication & Authorization:**
    *   Set up Django's built-in authentication views/URLs.
    *   Implement role-based access control (e.g., decorators, middleware).
2.  **Asset Views (`assets/views.py`):**
    *   Implement `AssetListView`, `AssetDetailView`, `AssetCreateView`, `AssetUpdateView`, `AssetDeleteView`.
    *   Ensure views enforce role permissions correctly.
3.  **Templates (`assets/templates/assets/`):**
    *   Create HTML templates (`asset_list.html`, `asset_detail.html`, `asset_form.html`, `asset_confirm_delete.html`, `base.html`).
    *   Integrate a CSS framework.
4.  **URL Routing (`assets/urls.py`, `it_asset_manager/urls.py`):**
    *   Define URL patterns for auth and asset views.
5.  **Testing (Phase 2):**
    *   **Auth Tests (`assets/tests/test_auth.py`):** Test login, logout, and access restrictions for different roles (e.g., Viewer cannot access create/update/delete views). Use Django's test client.
    *   **View Tests (`assets/tests/test_views.py`):** Write unit tests for each view:
        *   Verify correct template rendering.
        *   Test context data passed to templates.
        *   Test successful form submissions (create/update).
        *   Test object deletion.
        *   Test permission enforcement logic within views.
    *   **Template Tests:** Check for basic rendering and presence of key elements (can be part of view tests or manual checks).

**Phase 3: Renewal Alert System**

1.  **Email Configuration:**
    *   Configure email backend in `settings.py`.
2.  **Management Command (`assets/management/commands/check_renewals.py`):**
    *   Implement logic to find expiring assets (90, 60, 30 days).
    *   Implement logic to format and send emails.
3.  **Scheduling:**
    *   Set up Cron/Task Scheduler or Celery + Celery Beat to run `check_renewals` daily.
4.  **Testing (Phase 3):**
    *   **Command Tests (`assets/tests/test_commands.py`):**
        *   Unit test the logic for identifying expiring assets using mock dates/data.
        *   Test email formatting logic.
        *   Use Django's `mail.outbox` or mocking libraries (like `unittest.mock`) to test that emails *would* be sent correctly without actually sending them during tests.
    *   **Scheduling Tests:** Verify the scheduling mechanism triggers the command (often done manually or via integration tests in a staging environment).

**Phase 4: Dashboard & Refinements**

1.  **Dashboard View:**
    *   Create view/template summarizing expiring assets and other stats.
2.  **UI Improvements:**
    *   Add filtering, sorting, pagination to `AssetListView`.
3.  **Testing (Phase 4):**
    *   **Dashboard View Tests:** Test the logic for calculating dashboard statistics and context data.
    *   **Integration/End-to-End Tests:** Consider using tools like Selenium or Django's `LiveServerTestCase` to test complete user workflows (e.g., login -> view assets -> add asset -> check dashboard -> logout).
    *   **Refinement Tests:** Add specific tests for new UI features like filtering/sorting.

**Technology Stack Summary:**

*   **Backend Framework:** Python / Django
*   **Database:** Supabase (PostgreSQL)
*   **Frontend:** Django Templates + CSS Framework (e.g., Bootstrap)
*   **Task Scheduling:** Cron / Task Scheduler or Celery + Broker
*   **Email:** Django Email Backend + SMTP Service
*   **Testing:** Django Test Framework (`unittest`), potentially `pytest-django`, `unittest.mock`.

**Architecture Diagram (Conceptual):**

```mermaid
graph TD
    subgraph User Interface
        U[User Browser]
    end

    subgraph Web Server (Django Application)
        A[Django Views/Templates]
        B[Django ORM]
        C[Django Auth/RBAC]
        D[Renewal Check Command]
        E[Email Sending Module]
        T[Testing Framework]
    end

    subgraph Backend Services
        F[Supabase DB (PostgreSQL)]
        G[Task Scheduler (Cron/Celery Beat)]
        H[Email Service (SMTP)]
    end

    U -->|HTTP Requests| A;
    A -->|Login/Role Checks| C;
    A -->|CRUD Operations/Queries| B;
    C -->|User/Role Data| B;
    B -->|SQL Queries| F;
    F -->|Data| B;

    G -->|Triggers Daily| D;
    D -->|Query Expiring Assets| B;
    D -->|Sends Alert Details| E;
    E -->|Sends Email| H;

    T -->|Tests| A;
    T -->|Tests| B;
    T -->|Tests| C;
    T -->|Tests| D;
    T -->|Tests| E;
    T -->|Mocks/Interacts| F;
    T -->|Mocks/Interacts| H;