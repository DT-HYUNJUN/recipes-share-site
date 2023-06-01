from django.urls import reverse_lazy, reverse
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView, UpdateView
from communities.models import *
from communities.forms import *
from django.shortcuts import get_object_or_404, redirect



class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'communities/post_detail.html'
    pk_url_kwarg = 'post_pk'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post_pk = self.kwargs['post_pk']
    #     post = get_object_or_404(Post, pk=post_pk)
    #     context['post'] = post
    #     return context
    
    # def form_valid(self, form):
    #     post_pk = self.kwargs['post_pk']
    #     post = get_object_or_404(Post, pk=post_pk)
    #     comment = form.save(commit=False)
    #     comment.user = self.request.user
    #     comment.post = post
    #     comment.save()
    #     return redirect('communities:detail', post_pk=post_pk)
    
    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        recipe_pk = jsonObject.get('pk')
        content = jsonObject.get('content')
        review = Comment.objects.create(
            post = Post.objects.get(pk=recipe_pk),
            user = request.user,
            content = content
        )
        review.save()
        if review.user.profile_image:
            profile_image = review.user.profile_image.url
        else:
            profile_image = None
        context = {
            'review_pk': review.pk,
            'user': review.user.pk,
            'nickname': review.user.nickname,
            'profile_image': profile_image,
            'content': review.content,
            'created_at': review.created_at,
            'updated_at': review.updated_at
        }
        return JsonResponse(context)
    
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         post_pk = kwargs['post_pk']
    #         post = Post.objects.get(pk=post_pk)
    #         comment = form.save(commit=False)
    #         comment.user = request.user
    #         comment.post = post
    #         comment.save()
    #         context = {
    #             'username': comment.user.username,
    #             'content': comment.content,
    #             'success_url': reverse('communities:detail', kwargs={'post_pk': comment.post.pk})

    #         }
    #         return JsonResponse(context)
    #         # return redirect(self.get_success_url())
    #     else:
    #         return JsonResponse({'message': 'error',}, status=400)
        
    # def get_success_url(self):
    #     return reverse('communities:detail', kwargs={'post_pk': self.post.pk})
    
    

class CommentUpdateView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'communities/comment_update.html'
    pk_url_kwarg = 'comment_pk'

    def test_func(self):
        comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
        user = self.request.user
        return (comment.user == user) or user.is_superuser or user.is_staff

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        post = comment.post
        context['post'] = post
        return context
    
    # def post(self, request,*args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         comment = self.get_object()  
    #         comment.user = request.user
    #         comment.content = form.cleaned_data['content'] 
    #         comment.post = self.get_object().post
    #         comment.save()
    #         context = {
    #             'username': comment.user.username,
    #             'content': comment.content,
    #         }
    #         return redirect(self.get_success_url())
    #     else:
    #         return JsonResponse({'message': 'error',}, status=400)
    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        review_pk = jsonObject.get('pk')
        content = jsonObject.get('content')
        review = Comment.objects.get(pk=review_pk)

        if review.user == request.user:
            if review is not None:
                review.content=jsonObject.get('content')
                review.save()
                context = {
                    'content': content
                }
                return JsonResponse(context)
            return JsonResponse({'result': 'error!'}, status=400)
        else:
            raise PermissionDenied()
        
    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
        return reverse_lazy('communities:detail', kwargs={'post_pk': comment.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'


    def test_func(self):
        comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
        return self.request.user == comment.user
    
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    # def get_success_url(self):
    #     comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
    #     return reverse_lazy('communities:detail', kwargs={'post_pk': comment.post.pk})

    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        review = Comment.objects.get(pk=jsonObject.get('review_pk'))
        if review is not None:
            review.delete()
            return JsonResponse({'result': 'success'})
        return JsonResponse({'result': 'fail'})