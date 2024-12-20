from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'caption', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your caption here...', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
