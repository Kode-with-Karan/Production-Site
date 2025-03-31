from django import forms
from .models import Blog, Comment

# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ['title', 'content', 'category', 'tags', 'cover_image', 'status']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'content': forms.Textarea(attrs={'class': 'form-control'}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
#             'status': forms.Select(attrs={'class': 'form-control'}),
#         }

from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 
                  'banner_image', 'main_image', 'optional_image1', 
                  'optional_image2', 'optional_image3', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
