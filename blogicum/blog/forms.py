from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comment, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'last_name')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'last_name')