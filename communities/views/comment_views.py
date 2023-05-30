from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView, UpdateView
from communities.models import *
from communities.forms import *
from django.shortcuts import get_object_or_404, redirect



class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'communities/comment_create.html'


    def get_success_url(self):
        return reverse('communities:post_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)
        context['post'] = post
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            post_pk = kwargs['post_pk']
            post = Post.objects.get(pk=post_pk)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            context = {
                'username': comment.user.username,
                'content': comment.content,
            }
            # return JsonResponse(context)
            return redirect(self.get_success_url())
        else:
            return JsonResponse({'message': 'error',}, status=400)


class CommentUpdateView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'communities/comment_update.html'
    pk_url_kwarg = 'comment_pk'

    def test_func(self):
        comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
        user = self.request.user
        return (comment.user == user) or user.is_superuser or user.is_staff


    def get_success_url(self):
        comment_pk = self.kwargs['comment_pk']
        return reverse_lazy('communities:post_list')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        post = comment.post
        context['post'] = post
        return context
    
    def post(self, request,*args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            comment = self.get_object()  
            comment.user = request.user
            comment.content = form.cleaned_data['content'] 
            comment.post = self.get_object().post
            comment.save()
            context = {
                'username': comment.user.username,
                'content': comment.content,
            }
            return redirect(self.get_success_url())
        else:
            return JsonResponse({'message': 'error',}, status=400)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'


    def test_func(self):
        comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
        return self.request.user == comment.user
    

    def get_success_url(self):
        return reverse_lazy('communities:post_list')
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)