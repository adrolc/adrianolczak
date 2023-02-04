from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # Login/Register
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # Password change
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    # Password reset
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]