from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from communities.models import Post, Comment
from recipes.models import Recipe, RecipeReview
from .models import UserIngredient


class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']


    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


class PaginationInline(admin.TabularInline):
    template = 'tabular_paginated.html'
    per_page = 10
    extra = 0
    can_delete = False
    model = None

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(PaginationInline, self).get_formset(
            request, obj, **kwargs)


        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('page', ['0'])[0])
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.page = page
                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list


        PaginationFormSet.per_page = self.per_page

        return PaginationFormSet


class FridgeInline(PaginationInline):
    model = UserIngredient
    extra = 1


class PostInline(PaginationInline):
    model = Post
    fields = ('title',)
    extra = 1


class CommentInline(PaginationInline):
    model = Comment
    extra = 1


class RecipeInline(PaginationInline):
    model = Recipe
    fields = ('title',)
    extra = 0


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    fieldsets = UserAdmin.fieldsets + (
        ('추가정보', {"fields": ('nickname', 'profile_image', 'birthdate'),}),
    )
    inlines = (
        FridgeInline,
        PostInline,
        CommentInline,
        RecipeInline,
    )


admin.site.register(get_user_model(), CustomUserAdmin)