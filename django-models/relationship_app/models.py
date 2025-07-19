from django.db import models

# Create your models here.
'''
This file contains the models for the relationship application.
Author Model:
name: CharField.
Book Model:
title: CharField.
author: ForeignKey to Author.
Library Model:
name: CharField.
books: ManyToManyField to Book.
Librarian Model:
name: CharField.
library: OneToOneField to Library.

'''

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="libraries")
    
    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")
    
    def __str__(self):
        return self.name