from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import View
from django.urls import reverse_lazy
from . import forms
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

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

# Change password
class UserPasswordChangeView(PasswordChangeView):
    form_class = forms.ChangePasswordForm
    success_url = reverse_lazy("account:password_change_done")
    template_name = 'account/pages/password_change_form.html'

class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'account/pages/password_change_done.html'

# User profile
class UserProfileView(LoginRequiredMixin, View):
    def common_function(self, request):
        user = request.user
        user_form = forms.UserEditForm(instance=user)
        user_profile_form = forms.ProfileEditForm(data={
            'bio': user.profile.bio,
            'website_link': user.profile.website_link,
            'github_link': user.profile.github_link,
            'twitter_link': user.profile.twitter_link,
            'instagram_link': user.profile.instagram_link,
            'facebook_link': user.profile.facebook_link,
        })
        context = {
            'user_form': user_form,
            'user_profile_form': user_profile_form,
        }
        return context

    def get(self, request):
        context = self.common_function(request)
        return render(request, 'account/pages/user_profile.html', context)
    
    def post(self, request):
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        user_profile_form = forms.ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            context = self.common_function(request)
            return render(request, 'account/pages/user_profile.html', context)
        context = self.common_function(request)
        context['user_form'] = user_form
        return render(request, 'account/pages/user_profile.html', context)