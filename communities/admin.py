from django.contrib import admin
from accounts.admin import PaginationInline
from .models import *


class CommentInline(PaginationInline):
    model = Comment


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CommentInline, ImageInline)


admin.site.register(Post, PostAdmin)