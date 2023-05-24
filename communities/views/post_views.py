from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, ListView, UpdateView
from communities.models import *
from communities.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages



# Create your views here.

class PostListView(TemplateView):
    template_name = 'communities/post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

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
    template_name = 'communities/post_list.html'
    
    # def get_object(self, queryset=None):
    #     # 현재 로그인한 사용자의 게시물만 삭제 가능하도록 설정
    #     obj = super().get_object(queryset=queryset)
    #     if not obj.user == self.request.user:
    #         raise Http404
    #     return obj
    

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

    def get_success_url(self):
        return reverse_lazy('communities:post_list')

    def get_object(self, queryset=None):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        return post
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        messages.success(request, _('포스트가 삭제되었습니다.'))
        return super().delete(request, *args, **kwargs)