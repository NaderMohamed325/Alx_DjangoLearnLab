from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']



class ExampleForm(forms.ModelForm):
    name=forms.CharField(max_length=100)