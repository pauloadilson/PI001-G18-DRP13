from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
