from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, View, UpdateView, ListView
from communities.models import *
from communities.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse



# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'communities/post_list.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['comments'] = Comment.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        for post in queryset:
            post.comments = Comment.objects.filter(post=post.pk)
        return queryset

# class PostListView(TemplateView):
#     template_name = 'communities/post_list.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts'] = Post.objects.all()
#         context['comments'] = Comment.objects.filter(post=post.pk)

#         return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'communities/post_create.html'
    success_url = reverse_lazy('communities:post_list')
    
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
    def post(self, request, *args, **kwargs):
        post_pk = kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        if post.like_posts.filter(pk=request.user.pk).exists():
            post.like_posts.remove(request.user)
            like = False
        else:
            post.like_posts.add(request.user)
            like = True
        context = {
            'like': like,
        }
        return JsonResponse(context)
    
    
    # model = Post
    # form_class = PostForm
    # template_name = 'communities/post_update.html'
    # context_object_name = 'post'
    # success_url = reverse_lazy('communities:post_list')
    
    # def test_func(self):
    #     post = self.get_object()
    #     return self.request.user == post.user
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     post = self.get_object()
    #     context
        
    # def form_valid(self, form, formset):
    #     post = form.save()
    #     instances = formset.save(commit=False)
    #     for instance in instances:
    #         instance.post = post 
    #         instance.save()
    #     formset.save()
        
    
    # def get_object(self, queryset=None):
    #     post_pk = self.kwargs.get('post_pk')  # 혹은 'post_pk'로 수정해야 할 수도 있음
    #     post = get_object_or_404(Post, pk=post_pk, user=self.request.user)
    #     return post
            
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
        
    #     if form.is_valid():
    #         return self.form_valid(form, formset)
    #     else:
    #         return self.form_invalid(form, formset)