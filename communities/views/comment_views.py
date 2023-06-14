import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from communities.forms import *
from communities.models import *


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'communities/post_detail.html'
    pk_url_kwarg = 'post_pk'

    
    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        post_pk = jsonObject.get('pk')
        content = jsonObject.get('content')
        comment = Comment.objects.create(
            post = Post.objects.get(pk=post_pk),
            user = request.user,
            content = content
        )
        comment.save()
        if comment.user.profile_image:
            profile_image = comment.user.profile_image.url
        else:
            profile_image = None
        context = {
            'review_pk': comment.pk,
            'user': comment.user.pk,
            'nickname': comment.user.nickname,
            'profile_image': profile_image,
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at
        }
        return JsonResponse(context)


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


    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        review = Comment.objects.get(pk=jsonObject.get('review_pk'))
        if review is not None:
            review.delete()
            return JsonResponse({'result': 'success'})
        return JsonResponse({'result': 'fail'})