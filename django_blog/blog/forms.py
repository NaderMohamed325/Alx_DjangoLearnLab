# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag

class UserRegisterForm(UserCreationForm):
    """Extended user registration form with email field."""
    email = forms.EmailField()  # Add email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields in the form

class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts with tag support.

    Tags are entered as a comma-separated list in a single text field.
    """
    tags_input = forms.CharField(
        required=False,
        label='Tags',
        help_text='Comma separated list (e.g. django, web, tutorial)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'django, python, web'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_input']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post here...', 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Prefill tags_input with existing tags
            self.fields['tags_input'].initial = ', '.join(self.instance.tags.values_list('name', flat=True))

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        # Process tags
        tags_text = self.cleaned_data.get('tags_input', '')
        tag_names = [t.strip() for t in tags_text.split(',') if t.strip()]
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        # Set tags after instance has PK
        instance.tags.set(tags)
        return instance

class CommentForm(forms.ModelForm):
    """Form for creating and updating comments on blog posts."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your comment here...', 
                'rows': 3
            }),
        }
        labels = {
            'content': 'Comment'
        }
