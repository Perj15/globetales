from django.urls import path
from . import views
from .views import newsfeed, home, login_view, index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),  # Set the home view as the default
    path('index/', index, name='index'),  # Add this line for the index view
    path('profile/<str:username>/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('like_post/<int:pk>/', views.like_post, name='like_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('newsfeed/', newsfeed, name='newsfeed'),
    path('login/', login_view, name='login'),  # Ensure you have a login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
]
