# Contributing to IT Asset Manager

Thank you for considering contributing to the IT Asset Manager! This document outlines the process for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/web-app-centralizing.git
   cd web-app-centralizing
   ```
3. Add the original repo as an upstream remote:
   ```bash
   git remote add upstream https://github.com/Batu1-1an/web-app-centralizing.git
   ```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL (or SQLite for local development)
- pip and venv

### Local Setup

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your local settings (SQLite works out of the box for development)

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### Docker Setup (Alternative)

```bash
# Edit .env with your settings, then:
docker compose up --build
```

## Project Structure

```
web-app-centralizing/
├── assets/                   # Core IT asset management app
│   ├── management/commands/  # Custom management commands
│   ├── migrations/           # Database migrations
│   ├── templates/assets/     # App templates (Bootstrap 5.3)
│   └── tests/                # Test suite
├── it_asset_manager/         # Django project configuration
├── templates/registration/   # Auth templates
├── docs/                     # Documentation
├── Dockerfile                # Production container build
├── docker-compose.yml        # Orchestration with PostgreSQL
├── requirements.txt          # Python dependencies
└── .env.example              # Environment variable template
```

## Coding Standards

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/) style guide. Use `black` and `ruff` for formatting and linting.
- **Django**: Follow Django's [coding style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/).
- **Imports**: Group standard library, third-party, and local imports with a blank line between groups.
- **Templates**: Use consistent indentation (2 spaces) and descriptive block names.
- **Security**: Never commit secrets, keys, or credentials. Use environment variables for all sensitive data.

## Testing

All tests live in `assets/tests/`. Run the full suite with:

```bash
python manage.py test assets
```

### Writing Tests

- Add test methods to the appropriate module (`test_models.py`, `test_views.py`, `test_auth.py`, or `test_commands.py`).
- Use Django's `TestCase` and factory methods for database-dependent tests.
- Mock external services (email, APIs) to keep tests fast and deterministic.
- Ensure new features include tests for both happy paths and edge cases.

### Test Coverage Goals

- **Models**: 100% of field constraints, defaults, string representations, and custom methods.
- **Views**: Template rendering, form submission success/failure, redirect behavior.
- **Auth**: Login-required gates, role-based (Admin vs. Viewer) enforcement.
- **Commands**: Dry-run output, default parameters, custom arguments.

## Pull Request Process

1. Create a feature branch from `master`:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes with clear, descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` a new feature
   - `fix:` a bug fix
   - `docs:` documentation changes
   - `test:` adding or updating tests
   - `refactor:` code changes that neither fix bugs nor add features
   - `style:` formatting, missing semicolons, etc. (no code change)
   - `chore:` maintenance tasks
3. Run the full test suite and ensure all tests pass.
4. Push your branch and open a pull request against `master`.
5. In the PR description, explain what your changes do and why they're valuable.
6. Ensure the CI pipeline passes (if configured).
7. Request review from a maintainer.

### PR Checklist

- [ ] Tests pass (`python manage.py test assets`)
- [ ] New tests added for any new functionality
- [ ] No new warnings or linting issues
- [ ] Environment variables documented in `.env.example` if added
- [ ] CHANGELOG.md updated under "Unreleased"
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)

## Reporting Issues

- Search existing issues to avoid duplicates.
- Use a clear, descriptive title.
- Include steps to reproduce, expected behavior, and actual behavior.
- Include environment details (OS, Python version, Django version).
- Attach relevant logs or screenshots if applicable.
