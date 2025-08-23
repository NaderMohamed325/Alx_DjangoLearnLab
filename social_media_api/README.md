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
