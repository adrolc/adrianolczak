from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
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
        'id': 'register_email',
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
        'id': 'reset_password1',
    }))
    new_password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'reset_password2',
    }))

# Change password
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'old_password',
    }))
    new_password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'change_password1',
    }))
    new_password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'change_password2',
    }))



# Edit User/Profile
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'id': f'user_edit_{field}'})

    def clean_email(self):
        email = self.cleaned_data['email']
        user = self.instance
        if not email:
            raise forms.ValidationError("Email cannot be empty")
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise forms.ValidationError("Email already exists")
        return email

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'website_link', 'github_link', 'twitter_link', 'instagram_link', 'facebook_link')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget = forms.Textarea()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'id': f'user_profile_edit_{field}'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control d-none'})
        self.fields['bio'].widget.attrs.update({'rows': '4', 'maxlength': 150})