from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, View, UpdateView, ListView, DetailView
from communities.models import *
from communities.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse


class PostListView(ListView):
    model = Post
    template_name = 'communities/post_list.html'
    paginate_by = 10
    context_object_name = 'posts'
    queryset = Post.objects.prefetch_related('user', 'like_posts', 'posts').order_by('-pk')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        context['pagelist'] = pagelist
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'communities/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        post = context['post']
        prev_posts = Post.objects.filter(pk__lt=post.pk).order_by('-pk')[:2]
        next_posts = Post.objects.filter(pk__gt=post.pk).order_by('pk')[:2]
        adj_posts = list(prev_posts) + list(next_posts)
        comments = Comment.objects.prefetch_related('user').filter(post=post)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['adj_posts'] = adj_posts

        return context


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'communities/post_create.html'
    success_url = reverse_lazy('communities:post_list')

    def test_func(self):
        return self.request.user.is_authenticated 
    
    def form_valid(self, form):
        post = form.save(commit=False)  
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_pk'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

    def get_success_url(self):
        return reverse_lazy('communities:post_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
   
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'communities/post_update.html'
    pk_url_kwarg = 'post_pk'


    def test_func(self):
        review = Post.objects.get(pk=self.kwargs['post_pk'])
        user = self.request.user
        return (review.user == user) or user.is_superuser or user.is_staff


    def get_success_url(self):
        post_pk = self.kwargs['post_pk']
        return reverse_lazy('communities:post_list')


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)

        if post.like_posts.filter(pk=request.user.pk).exists():
            post.like_posts.remove(request.user)
            is_liked = False
        else:
            post.like_posts.add(request.user)
            is_liked = True

        context = {
            'is_liked': is_liked,
        }
        return JsonResponse(context)