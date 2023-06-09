from django.contrib import admin
from accounts.admin import PaginationInline
from .models import *


class CommentInline(PaginationInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CommentInline,)


admin.site.register(Post, PostAdmin)