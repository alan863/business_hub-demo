from django import forms 
from django.contrib.auth.forms import UserCreationForm
from  .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SearchUserForm(forms.Form):
    id = forms.CharField()
   