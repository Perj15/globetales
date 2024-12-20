from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure 'login' matches your login URL name
    return newsfeed(request)

def newsfeed(request):
    sort_by = request.GET.get('sort', 'latest')  # Default to latest
    search_query = request.GET.get('search', '')
    posts = Post.objects.all()
    
    if search_query:
        posts = posts.filter(
            Q(author__username__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(caption__icontains=search_query)
        )
    
    if sort_by == 'latest':
        posts = posts.order_by('-created_at')  # Most recent first
    elif sort_by == 'oldest':
        posts = posts.order_by('created_at')  # Oldest first
    elif sort_by == 'popular':
        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count')  # Most liked first
    else:
        posts = posts.order_by('-created_at')  # Fallback to latest

    context = {
        'posts': posts,
        'user': request.user,
        'search_query': search_query,
    }
    return render(request, 'blog/newsfeed.html', context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    if request.user != user:
        return HttpResponseForbidden()
    return render(request, 'blog/profile.html', {'user': user, 'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    post.delete()
    return redirect('index')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post
    })

def home(request):
    if request.user.is_authenticated:
        return redirect('newsfeed')  # Redirect to the newsfeed if logged in
    else:
        return redirect('login')  # Redirect to login page if not logged in

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('newsfeed')  # Redirect to newsfeed after login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
