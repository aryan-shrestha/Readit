from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body', 'category', 'slang']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control custom-input'}),
                   'slang': forms.TextInput(attrs={'placeholder': "use ' _ ' instead of spaces "})
                   }

class CustomUserCreationForm(forms.Form):
    first_name = forms.CharField(label="First Name", min_length=4, max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username", min_length=4, max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Enter Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already Exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class UserProfilePicForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['profile_pic']