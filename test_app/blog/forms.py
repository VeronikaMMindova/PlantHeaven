from django import forms
from .models import Post, Category, Comment, Plant

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for choice in choices:
    choice_list.append(choice)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'category', 'description', 'snippet')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a description...',
                'rows': 5
            }),
            'snippet': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'description', 'snippet', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
        }


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'habitat', 'image', 'wikipedia_url', 'category', 'type_of_plant']

    widgets = {
        'name': forms.TextInput(attrs={'placeholder': 'Plant Name'}),
        'habitat': forms.TextInput(attrs={'placeholder': 'Habitat'}),
        'wikipedia_url': forms.URLInput(attrs={'placeholder': 'Wikipedia URL (optional)'}),
        'type_of_plant': forms.Select(),
        'category': forms.Select(),
        'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    }