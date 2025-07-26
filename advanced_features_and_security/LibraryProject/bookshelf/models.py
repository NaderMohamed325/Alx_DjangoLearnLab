from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    publication_year=models.IntegerField()
    
'''
date_of_birth: A date field.
profile_photo: An image field.
'''        
class CustomUser(AbstractUser):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    date_of_birth=models.DateField()
    profile_photo=models.ImageField(upload_to='userPhoto/',blank=True,null=True)
        
    