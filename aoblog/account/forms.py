from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import Profile

# Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'login_username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'login_password'
    }))


# Register
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'register_username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'register_username',
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'register_password1',
    }))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'register_password2',
    }))

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use")
        return data


# Reset password
class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'reset_password_email',
    }))

class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'register_password1',
    }))
    new_password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'register_password2',
    }))

# Profile
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)