# Django Blog Project

A full-featured Django blog application with user authentication and CRUD operations for blog posts.

## Features

### User Authentication

- User registration with email
- Login and logout functionality
- User profile viewing

### Blog Post Management

- View all posts with pagination
- View individual post details
- Create new posts (authenticated users only)
- Edit posts (author only)
- Delete posts (author only)

## Project Structure

The project follows Django's MVT (Model-View-Template) architecture:

### Models

- `User` - Django's built-in User model for authentication
- `Post` - Custom model for blog posts

### Views

- Authentication views (register, login, logout, profile)
- CRUD operations for posts using class-based views

### Templates

- Base template with common layout elements
- Authentication templates (login, register, etc.)
- Blog post templates (list, detail, form, delete confirmation)

## URL Structure

- `/register/` - Register a new user
- `/login/` - Log in
- `/logout/` - Log out
- `/profile/` - View user profile
- `/home/` or `/` - Home page
- `/posts/` - List all blog posts
- `/posts/<id>/` - View a specific post
- `/posts/new/` - Create a new post (login required)
- `/posts/<id>/edit/` - Edit a post (author only)
- `/posts/<id>/delete/` - Delete a post (author only)

## Security and Permissions

- Anonymous users can view posts but cannot create, edit, or delete them
- Authenticated users can create new posts
- Only the author of a post can edit or delete it
- LoginRequiredMixin and UserPassesTestMixin are used to enforce these permissions

## Setup and Installation

1. Clone the repository
2. Install dependencies from requirements.txt
3. Run migrations
4. Create a superuser
5. Run the development server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Further Development Ideas

- Add comments to posts
- Implement categories and tags
- Add search functionality
- Implement post likes/ratings
- Add user profile pictures
