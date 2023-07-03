from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm#, UserChangeForm

from .models import Account

class AuthenticateForm(forms.ModelForm):
    email = forms.EmailField(
        label = 'Email',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Account
        fields = (
            'email',
            'password',
        )

    def clean(self, *args, **kwargs):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if not user.is_active:
                    raise forms.ValidationError('This user has been disabled')
            else:
                raise forms.ValidationError('Invalid login')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label = 'Email',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    password1 = forms.CharField(
        required = True,
        label = 'Password',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id': 'password-input',
            }
        )
    )

    password2 = forms.CharField(
        required = True,
        label = 'Confirm password',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Account
        fields = (
            'email',
            'password1',
            'password2',
        )