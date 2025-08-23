# Social Media API

## Overview

A minimal social media API starter focusing on user registration, authentication (token-based), and profile management.

## Custom User Model

Extends `AbstractUser` with:

- bio (TextField, optional)
- profile_picture (ImageField, optional)
- followers (ManyToMany to self, asymmetrical) with reverse `following`

`AUTH_USER_MODEL = 'accounts.User'` is set in `settings.py`.

## Authentication

Token authentication via `rest_framework.authtoken`.

Default DRF auth classes (Token + Session). Default permission: authenticated users.

### Endpoints (all prefixed with `/api/accounts/`)

- POST `register/` : register new user, returns user data + token
- POST `login/` : login with username & password, returns user data + token
- GET `profile/` : retrieve authenticated user profile
- PUT/PATCH `profile/` : update profile fields (first_name, last_name, bio, profile_picture)

## Sample Requests

### Register

```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "StrongPass123!",
  "password2": "StrongPass123!",
  "first_name": "Alice",
  "last_name": "Doe"
}
```

Response: `201 Created`

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Doe",
  "bio": null,
  "profile_picture": null,
  "followers_count": 0,
  "following_count": 0,
  "token": "<token>"
}
```

### Login

```http
POST /api/accounts/login/
Content-Type: application/json

{
  "username": "alice",
  "password": "StrongPass123!"
}
```

Response includes token.

### Auth Header

`Authorization: Token <token>`

## Setup

1. Install dependencies (ensure Django + djangorestframework + Pillow installed)
2. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser (optional): `python manage.py createsuperuser`
4. Run server: `python manage.py runserver`

## Media Files

Uploaded profile pictures stored under `media/profile_pics/`.

## Tests

Basic auth flow test exists in `accounts/tests.py` covering register, login, profile.

## Next Steps

- Add follower/unfollower endpoints
- Add pagination and throttling
- Add tests for auth workflows

## Posts & Comments API

### Endpoints

All routes require authentication (Token) unless read-only.

Posts:

- GET /api/posts/ (list, supports ?search=term, ?ordering=created_at)
- POST /api/posts/ (create)
- GET /api/posts/{id}/ (retrieve)
- PUT/PATCH /api/posts/{id}/ (update if owner)
- DELETE /api/posts/{id}/ (delete if owner)

Comments:

- GET /api/comments/ (list)
- POST /api/comments/ (create)
- GET /api/comments/{id}/
- PUT/PATCH /api/comments/{id}/ (owner only)
- DELETE /api/comments/{id}/ (owner only)

### Sample Create Post

```http
POST /api/posts/
Authorization: Token <token>
Content-Type: application/json

{
  "title": "First Post",
  "content": "Hello world"
}
```

### Sample Create Comment

```http
POST /api/comments/
Authorization: Token <token>
Content-Type: application/json

{
  "post": 1,
  "content": "Nice post!"
}
```

Pagination: add ?page=2&page_size=5

Filtering/Search: ?search=hello (title or content)

## Follow System & Feed

### Follow Endpoints

- POST /api/accounts/follow/{user_id}/ – follow a user
- POST /api/accounts/unfollow/{user_id}/ – unfollow a user

Responses include a simple confirmation message. Self-follow/unfollow is blocked.

### Feed Endpoint

- GET /api/feed/ – returns recent posts (max 100) authored by users the authenticated user follows, newest first.

Example:

```http
GET /api/feed/
Authorization: Token <token>
```

### Notes

- To populate your feed, follow some users first.
- Consider extending feed with pagination later.

## Deployment (Production)

### Environment Variables
Set these in your hosting provider (e.g. Heroku, Render, Railway):
- DJANGO_SECRET_KEY (required)
- DJANGO_DEBUG=false
- DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
- DJANGO_SECURE_SSL_REDIRECT=true
- DATABASE_URL (if using Postgres via dj-database-url or provider config)

### Static Files
Run: `python manage.py collectstatic` during build. Whitenoise serves files from `staticfiles/`.

### Gunicorn
Procfile: `web: gunicorn social_media_api.wsgi --log-file -`

### Database
Use Postgres in production. Update `DATABASES` via environment (you can integrate `dj-database-url` as an enhancement).

### Security
Security headers auto-enabled when DEBUG is false.

### Sample Heroku Steps
1. heroku create
2. heroku config:set DJANGO_SECRET_KEY=... DJANGO_ALLOWED_HOSTS=yourapp.herokuapp.com
3. git push heroku main
4. heroku run python manage.py migrate
5. heroku run python manage.py createsuperuser

### Monitoring
Add tools like Sentry (sentry-sdk) and enable logging aggregation.
