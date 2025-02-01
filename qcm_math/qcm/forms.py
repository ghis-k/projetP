from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    name = forms.CharField(max_length=100, required=True)
