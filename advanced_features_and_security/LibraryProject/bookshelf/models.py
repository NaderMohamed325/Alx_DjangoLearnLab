from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
# bookshelf/models.py

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()  
    description = models.TextField()  

    class Meta:
        permissions = [
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title

    
'''
date_of_birth: A date field.
profile_photo: An image field.
'''        
class CustomUser(AbstractUser):
    date_of_birth=models.DateField(blank=True,null=True)
    profile_photo=models.ImageField(upload_to='userPhoto/',blank=True,null=True)
        

class CustomUserManager(BaseUserManager):
        def create_user(self,email,username,date_of_birth=None,profile_photo=None,password=None,**extra_fields):
            if not email:
                raise ValueError("email Field is required")
            if not username:
                raise ValueError("username Field is required")
            email=self.normalize_email(email)
            user=self.model(
                username=username,
                email=email,
                date_of_birth=date_of_birth,
                profile_photo=profile_photo,
              **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
            
        def create_superuser(self, username, email, password=None, **extra_fields):
         extra_fields.setdefault('is_staff', True)
         extra_fields.setdefault('is_superuser', True)
         extra_fields.setdefault('is_active', True)

         if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
         if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

         return self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth='2000-01-01',  # default or required manually
            **extra_fields
         )
          
          
            