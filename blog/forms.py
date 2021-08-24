from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from blog.models import Post
class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-1'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-1'}), label='Confirm password (Again)')
    class Meta():
        model=User
        fields = ('first_name','last_name','username','email')
        labels = {'first_name':'First Name', 'last_name': 'Last Name', 'username':'Username','email':'Email'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control my-1'}),
            'last_name':forms.TextInput(attrs={'class':'form-control my-1'}),
            'username':forms.TextInput(attrs={'class':'form-control my-1'}),
            'email':forms.EmailInput(attrs={'class':'form-control my-1'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(label='Username', widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control my-2'}))
    password = forms.CharField(label='Password', strip= False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))

# for add post
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc']
        labels = {'title': 'Title', 'desc':'Description'}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control my-1'}),
            'desc':forms.Textarea(attrs={'class':'form-control my-1'})
        }