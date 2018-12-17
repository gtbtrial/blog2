from django.contrib import admin

# Register your models here.
from .models import BlogEntries

# admin.site.register(BlogEntries)

@admin.register(BlogEntries)
class BlogGrid(admin.ModelAdmin):
    list_display = ['title','blog_body','datetimeofentry','user_id']