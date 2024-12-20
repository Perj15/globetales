from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, ProfileUpdateForm
from blog.models import Post  # Correctly import the Post model from the blog app

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to GlobeTales!')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.error(request, "You cannot edit another user's profile.")
        return redirect('index')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user.user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=username)
    else:
        form = ProfileUpdateForm(instance=user.user_profile)

    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'form': form,
        'posts': posts,
        'profile_user': user,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_redirect(request):
    return redirect('profile', username=request.user.username)
