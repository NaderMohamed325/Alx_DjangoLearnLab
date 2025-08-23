# ALX Django Learn Lab

A multi-project repository showcasing Django and Django REST Framework (DRF) concepts, from fundamentals to advanced APIs, security, and testing. Each folder is a self-contained Django project you can run independently.

## Contents

- Introduction_to_Django/ — first steps with Django (models, CRUD, templates)
- django-models/ — modeling relationships and queries; extra templates and examples
- advanced_features_and_security/ — forms, authentication, role-based views, and security-minded features
- api_project/ — a basic DRF API and serializers
- advanced-api-project/ — a richer DRF API with filtering, search, ordering, token auth, and a comprehensive test suite
- django_blog/ — classic blog app with user auth & class-based CRUD views
- social_media_api/ — evolving social platform API (custom user, posts, follows, likes, notifications, deployment setup)

## Folder-by-folder guide

### 1. Introduction_to_Django/LibraryProject

Foundations of Django.

- Topics: project/app creation, settings, models, migrations, Django shell CRUD, admin registration.
- Key artifacts: `bookshelf/models.py` (Book model), CRUD markdown walkthroughs (`create.md`, `retrieve.md`, `update.md`, `delete.md`, `CRUD_operations.md`).
- Learning goals: understand MVC/MVT mapping, migrations lifecycle, admin customization basics.

### 2. django-models/LibraryProject

Focus on expanding model concepts (mirrors intro as a scaffold—extend here).

- Suggested extensions: relationships (FK, M2M, OneToOne), verbose names, model methods, advanced lookups, aggregation.
- Use it to experiment with more complex query patterns before applying them in API projects.

### 3. advanced_features_and_security/LibraryProject

Adds intermediate/advanced server-side features.

- Topics: forms & ModelForms, authentication flows, role or permission-based access, secure settings patterns, template organization.
- Potential enhancements: CSRF considerations, custom auth backends, rate limiting (via middleware or DRF throttle if integrated), messages framework, password reset flow.

### 4. api_project/

First REST-oriented project (baseline DRF usage).

- Topics: serializers (ModelSerializer), basic viewsets or APIViews, URL routing, simple validation, response formats, status codes.
- Goal: map plain Django models to REST endpoints with minimal extras.

### 5. advanced-api-project/

Production-style DRF patterns.

- Topics: filtering (`django-filter`), search & ordering backends, token auth, pagination (`PageNumberPagination`), permissions, test-driven development.
- Artifacts: `api/serializers.py`, `api/views.py`, `api/test_views.py`, `TESTING_DOCUMENTATION.md` (usage examples & test guidance).
- Learning goals: build maintainable, discoverable APIs with consistent query features.

### 6. django_blog/

Classic blog application with HTML templates and class-based views.

- Topics: user registration/login/logout, profile view, `LoginRequiredMixin`, `UserPassesTestMixin`, pagination in CBVs, CRUD patterns for posts.
- Extend with: tagging, comments, search, sitemap/feeds, caching.

### 7. social_media_api/

End-to-end social platform style API (most feature-rich app in the repo).

- Current features:
  - Custom user model (`accounts.User`) with bio, profile picture, asymmetric followers/following.
  - Token-based authentication (DRF authtoken) + profile update endpoints.
  - Posts & comments (CRUD, search, ordering, pagination).
  - Follow/unfollow endpoints & personalized feed (posts by followed users, newest first).
  - Likes (idempotent like/unlike with counts & user-liked flag in serializers).
  - Notifications (generic association: follow, like, comment events) with read flag.
  - Deployment readiness: environment-driven settings, Whitenoise static serving, Procfile (Gunicorn), security headers.
- Future enhancements: websockets (channels) for real-time notifications, rate limiting, richer notification verbs, hashtagging, media uploads for posts, async tasks (Celery) for fan-out.

### 8. Cross-cutting themes

- Environment & dependency management: Pipenv across projects, optional requirements files for deployment.
- Testing: progressive increase—unit & API tests emphasized in advanced API and (to expand) social media app.
- Security hardening: secure cookies, allowed hosts, static serving, auth patterns. Extend with CSP, HSTS, referrer policy, throttling.
- Documentation style: root README high-level; per-project READMEs for deep dives (some placeholders duplicated—refactor opportunity).

### 9. Suggested learning path

1. Start: `Introduction_to_Django` to grasp fundamentals.
2. Deepen: `django-models` for complex relationships.
3. Add UX & security: `advanced_features_and_security`.
4. Enter APIs: `api_project` (core DRF) then `advanced-api-project` (filters/tests/auth patterns).
5. Full-stack HTML example: `django_blog`.
6. Capstone: `social_media_api` (aggregate concepts + deployment).

### 10. Potential improvements (roadmap ideas)

- Consolidate duplicate intro READMEs (DRY).
- Add CI workflow for tests (GitHub Actions).
- Add Dockerfile + docker-compose for Postgres + Redis (prep for async tasks).
- Implement `dj-database-url` parsing and separate settings modules (dev/stage/prod).
- Expand notification system with websocket push (Channels) and batch read/unread endpoints.
- Add OpenAPI/Swagger schema (drf-spectacular or drf-yasg) across API projects.
- Introduce caching (per-view or low-level) for heavy read endpoints (feed, posts list).
- Add linting & formatting config (ruff / black / isort) and pre-commit hooks.

### 11. Reference quick map

| Folder                         | Theme                        | Key Skills                                                        |
| ------------------------------ | ---------------------------- | ----------------------------------------------------------------- |
| Introduction_to_Django         | Fundamentals                 | Project/app setup, models, admin, CRUD shell                      |
| django-models                  | Advanced models              | Relationships, queries, aggregation                               |
| advanced_features_and_security | Intermediate server features | Forms, auth flows, permissions, security                          |
| api_project                    | Basic REST                   | Serializers, basic endpoints                                      |
| advanced-api-project           | Advanced REST                | Filtering, search, ordering, tests, auth                          |
| django_blog                    | Web app (templates)          | CBVs, auth, CRUD UI                                               |
| social_media_api               | Full feature API             | Custom user, social graph, feed, likes, notifications, deployment |

---

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

Below is a generic flow. Replace PLACEHOLDER_PROJECT_FOLDER with one of:

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

````powershell
$token = "<admin-token>"
curl -Method DELETE `
         -Uri "http://127.0.0.1:8000/api/books/delete/1/" `
         -Headers @{ Authorization = "Token $token" }
```text

Tokens can be created via Django admin (User -> Token) or with DRF’s command:

```powershell
python manage.py drf_create_token <username>
````

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

  ````powershell
  pip install django-filter

  ```text
  ````

- After changing models, always run migrations:

  ````powershell
  python manage.py makemigrations
  python manage.py migrate

  ```text
  ````

- Pagination warning (unordered queryset) is expected when listing without an explicit default ordering.

## License

No license file provided. Use at your discretion for learning purposes.
