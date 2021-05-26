from django import forms

from .models import *

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body', 'category', 'slang']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control custom-input'}),
                   'slang': forms.TextInput(attrs={'placeholder': "use ' _ ' instead of spaces "})
                   }

class UserProfilePicForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['profile_pic']