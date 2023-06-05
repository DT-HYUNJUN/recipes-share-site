from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, View, UpdateView, ListView, DetailView
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
    paginate_by = 10
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-pk')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'] = Post.objects.all()
        # context['comments'] = Comment.objects.all()
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        context['pagelist'] = pagelist
        return context
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     for post in queryset:
    #         post.comments = Comment.objects.filter(post=post.pk)
    #     return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'communities/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prev_posts = Post.objects.filter(pk__lt=self.object.pk).order_by('-pk')[:2]
        next_posts = Post.objects.filter(pk__gt=self.object.pk).order_by('pk')[:2]
        adj_posts = list(prev_posts) + list(next_posts)
        # context['posts'] = Post.objects.all()
        # context['comments'] = Comment.objects.all()
        post = Post.objects.get(pk=self.object.pk)
        comments = post.posts.all()
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['adj_posts'] = adj_posts

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
    # def post(self, request, *args, **kwargs):
    #     post_pk = kwargs['post_pk']
    #     post = Post.objects.get(pk=post_pk)
    #     if post.like_posts.filter(pk=request.user.pk).exists():
    #         post.like_posts.remove(request.user)
    #         like = False
    #     else:
    #         post.like_posts.add(request.user)
    #         like = True
    #     context = {
    #         'like': like,
    #     }
    #     return JsonResponse(context)
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