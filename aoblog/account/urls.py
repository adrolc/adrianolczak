from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # Password reset
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]