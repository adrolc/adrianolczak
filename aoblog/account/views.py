from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.views.generic import View
from django.urls import reverse_lazy
from . import forms
from .models import Profile

# Login
class UserLoginView(LoginView):
    template_name = 'account/pages/login.html'
    authentication_form = forms.LoginForm
    redirect_authenticated_user = True


# Logout
class UserLogoutView(LogoutView):
    pass


# Register
class UserRegisterView(View):
    def get(self, request):
        register_form = forms.RegisterForm()
        return render(request, 'account/pages/register.html', {'form': register_form})
    
    def post(self, request):
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            # Create user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/pages/register_done.html', {'user': new_user})
        return render(request, 'account/pages/register.html', {'form': register_form})


# Reset password
class UserPasswordResetView(PasswordResetView):
    template_name = 'account/pages/password_reset_form.html'
    email_template_name = 'email_templates/password_reset_email.html'
    form_class = forms.ResetPasswordForm
    success_url = reverse_lazy("account:password_reset_done")
    subject_template_name = "email_templates/password_reset_subject.txt"


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/pages/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = forms.SetNewPasswordForm
    template_name = 'account/pages/password_reset_confirm.html'
    success_url = reverse_lazy("account:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/pages/password_reset_complete.html'

