# Introduction_to_Django Project

Welcome to the **Introduction to Django** project. This project walks you through the fundamentals of Django, including setting up the development environment, defining and working with models, performing CRUD operations, and using the Django Admin interface.

---

## 📁 GitHub Repo Structure
```
Alx_DjangoLearnLab/
└── Introduction_to_Django/
    ├── LibraryProject/           # Django project directory
    ├── bookshelf/               # Django app directory
    ├── create.md                # Documented creation step
    ├── retrieve.md              # Documented retrieval step
    ├── update.md                # Documented update step
    ├── delete.md                # Documented deletion step
    ├── CRUD_operations.md       # Combined CRUD shell operations
    └── README.md                # This file
```

---

## 0️⃣ Django Development Environment Setup

### ✅ Install Django
```bash
pip install django
```

### ✅ Create the Django Project
```bash
django-admin startproject LibraryProject
```

### ✅ Navigate into the project directory
```bash
cd LibraryProject
```

### ✅ Create `README.md`
Create this file in the `LibraryProject` directory to track project progress.

### ✅ Run the Development Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

### ✅ Explore Project Structure
- **settings.py**: Configuration settings for the project.
- **urls.py**: Route definitions.
- **manage.py**: Utility to interact with Django commands.

---

## 1️⃣ Implementing and Interacting with Django Models

### ✅ Create the App
```bash
python manage.py startapp bookshelf
```

### ✅ Define the Book Model
Edit `bookshelf/models.py`:
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
```

### ✅ Register the App
Add `'bookshelf'` to `INSTALLED_APPS` in `LibraryProject/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'bookshelf',
]
```

### ✅ Migrate the Model
```bash
python manage.py makemigrations bookshelf
python manage.py migrate
```

### ✅ Django Shell CRUD Operations
```bash
python manage.py shell
```
Documented in:
- `create.md`
- `retrieve.md`
- `update.md`
- `delete.md`
- `CRUD_operations.md` (summary of all operations)

---

## 2️⃣ Utilizing the Django Admin Interface

### ✅ Create Superuser
```bash
python manage.py createsuperuser
```
Visit: http://127.0.0.1:8000/admin and log in.

### ✅ Register the Book Model in Admin
Edit `bookshelf/admin.py`:
```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author")
    list_filter = ("publication_year",)
```

---

## ✅ Summary
- 🧱 Set up Django and ran the dev server
- 📚 Created a model with migrations
- 💻 Performed CRUD operations via Django shell
- 🛠️ Registered and customized admin interface for data management

This structured project gives you foundational knowledge in Django development.

---

Let me know if you want to add forms, views, or connect this to a frontend.
