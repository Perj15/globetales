from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_redirect, name='profile_redirect'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='accounts/login.html',
             next_page='index'
         ), 
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
