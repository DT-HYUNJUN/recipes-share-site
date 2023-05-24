from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, ListView, UpdateView
from communities.models import *
from communities.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User



# Create your views here.

class PostListView(TemplateView):
    template_name = 'communities/post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'communities/post_create.html'
    success_url = reverse_lazy('communities:post_list')
    
    def form_valid(self, form):
        post = form.save(commit=False)

        # User 인스턴스 생성
        user = User(username='anonymous')  # 사용자명을 설정
        user.save()
        
        post.user = user
        post.save()
        
        # 로그인 기능 구현 후 이거 넣기 
        # post.user = self.request.user
        # post.save()
        return super().form_valid(form)
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('communities:post_list')
    
    def get_object(self, queryset=None):
        # 현재 로그인한 사용자의 게시물만 삭제 가능하도록 설정
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj
    
    