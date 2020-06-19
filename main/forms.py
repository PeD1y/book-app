from .models import User
from django import forms


class LoginForm(forms.Form):
    model = User
    username = forms.CharField()
    password = forms.CharField()