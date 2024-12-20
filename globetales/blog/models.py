from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

class Post(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    caption = models.TextField()
    image = models.ImageField(upload_to='posts/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

def __str__(self):
    return f"{self.title} by {self.author.username}"

@property
def like_count(self):
    return self.likes.count()
