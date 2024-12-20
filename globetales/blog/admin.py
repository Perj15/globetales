from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'caption', 'like_count', 'created_at')
