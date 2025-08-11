# ALX Django Learn Lab

A multi-project repository showcasing Django and Django REST Framework (DRF) concepts, from fundamentals to advanced APIs, security, and testing. Each folder is a self-contained Django project you can run independently.

## Contents

- Introduction_to_Django/ — first steps with Django (models, CRUD, templates)
- django-models/ — modeling relationships and queries; extra templates and examples
- advanced_features_and_security/ — forms, authentication, role-based views, and security-minded features
- api_project/ — a basic DRF API and serializers
- advanced-api-project/ — a richer DRF API with filtering, search, ordering, token auth, and a comprehensive test suite

## Requirements

- Python 3.12+
- Pipenv (preferred) or virtualenv/pip
- SQLite (bundled)

Key packages used in different projects:

- Django 5.2.x
- Django REST Framework
- django-filter
- djangorestframework-authtoken

## Quick start (choose a project)

Below is a generic flow. Replace <project-folder> with one of:

- advanced-api-project
- api_project
- advanced_features_and_security/LibraryProject
- django-models/LibraryProject
- Introduction_to_Django/LibraryProject

### 1) Setup environment and install deps (Pipenv)

```powershell
cd .\<project-folder>
pipenv install
pipenv shell
```

Alternative with venv + pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # if present, otherwise use Pipfile/Pipfile.lock via pipenv
```

### 2) Apply migrations and run the server

```powershell
python manage.py migrate
python manage.py runserver
```

### 3) Create a superuser (optional, for admin and token creation)

```powershell
python manage.py createsuperuser
```

## Project highlights

### advanced-api-project (DRF with filters/search/ordering + tests)

- App path: `advanced-api-project/api`
- Base API prefix: `/api/`
- Pagination: PageNumberPagination (PAGE_SIZE = 10)
- Auth: Session, Basic, and TokenAuthentication enabled
- Filtering and search via django-filter and DRF filters
- Comprehensive tests in `api/test_views.py` and guide in `TESTING_DOCUMENTATION.md`

Endpoints (relative to `/api/`):

- GET `books/` — list books
  - filterset fields: `title`, `author` (ID), `publication_year`
  - search fields: `title`, `author__name` via `?search=...`
  - ordering fields: `title`, `publication_year` via `?ordering=title` or `?ordering=-publication_year`
- GET `books/<id>/` — retrieve by ID
- POST `books/create/` — create (requires authentication)
- PATCH `books/update/<id>/` — partial update (requires authentication)
- DELETE `books/delete/<id>/` — delete (requires admin/staff)

Example requests (PowerShell curl examples):

List with search and ordering:

```powershell
curl "http://127.0.0.1:8000/api/books/?search=Orwell&ordering=title"
```

Create a book (Token auth):

```powershell
$token = "<your-token>"
curl -Method POST `
		 -Uri "http://127.0.0.1:8000/api/books/create/" `
		 -Headers @{ Authorization = "Token $token"; "Content-Type" = "application/json" } `
		 -Body (@{ title = "1984"; publication_year = 1949; author = 1 } | ConvertTo-Json)
```

Delete a book (admin only):

```powershell
$token = "<admin-token>"
curl -Method DELETE `
		 -Uri "http://127.0.0.1:8000/api/books/delete/1/" `
		 -Headers @{ Authorization = "Token $token" }
```

Tokens can be created via Django admin (User -> Token) or with DRF’s command:

```powershell
python manage.py drf_create_token <username>
```

Run tests (uses a separate test database automatically):

```powershell
python manage.py test api.test_views
```

### api_project (basic DRF API)

- App path: `api_project/api`
- Focus: models, serializers, simple views
- Run the same migrate/runserver flow and access endpoints via the configured `api_project/api/urls.py`

### advanced_features_and_security/LibraryProject

- Focus: authentication, forms, and role-based views; includes templates (login, register, etc.)
- App paths: `bookshelf/` and `relationship_app/`
- Templates under `bookshelf/templates/` and `relationship_app/templates/`

### django-models/LibraryProject

- Focus: model definitions, relationships, migrations; example templates and tests

### Introduction_to_Django/LibraryProject

- Focus: foundational Django app structure and CRUD examples

## Repository structure (abridged)

```
Alx_DjangoLearnLab/
├─ advanced-api-project/
│  ├─ manage.py
│  ├─ advanced_api_project/
│  └─ api/
├─ api_project/
│  ├─ manage.py
│  ├─ api_project/
│  └─ api/
├─ advanced_features_and_security/
│  └─ LibraryProject/
│     ├─ manage.py
│     ├─ bookshelf/
│     └─ relationship_app/
├─ django-models/
│  └─ LibraryProject/
│     ├─ manage.py
│     ├─ bookshelf/
│     └─ relationship_app/
└─ Introduction_to_Django/
	 └─ LibraryProject/
			├─ manage.py
			└─ bookshelf/
```

## Tips & troubleshooting

- If you see `ModuleNotFoundError: No module named 'django_filters'`, install:
  ```powershell
  pip install django-filter
  ```
- After changing models, always run migrations:
  ```powershell
  python manage.py makemigrations
  python manage.py migrate
  ```
- Pagination warning (unordered queryset) is expected when listing without an explicit default ordering.

## License

No license file provided. Use at your discretion for learning purposes.
