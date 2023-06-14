import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView, View, UpdateView, ListView, DetailView
from communities.models import *
from communities.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
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

        images = post.images.all()
        image_count = images.count()
        if image_count == 1:
            images = list(images) * 4
        elif image_count <= 3:
            images = list(images) * 2
        context['images'] = images
        return context


class PostCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'communities/post_create.html'


    def get(self, *args, **kwargs):
        form = PostForm()
        imageform = ImageForm()
        return self.render_to_response({
            'form': form,
            'imageform': imageform,
        })


    def post(self, *args, **kwargs):
        form = PostForm(self.request.POST)
        images = self.request.FILES.getlist('image')

        if form.is_valid():
            post = form.save(commit=False)
            post.user = self.request.user
            post.save()

            for image in images:
                if image:
                    Image.objects.create(post=post, image=image)
        
            return redirect('communities:detail', post_pk=post.pk)

        imageform = ImageForm()

        return self.render_to_response({
            'form': form,
            'imageform': imageform
        })


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


    def delete(self, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_pk'])
        media_dir = os.path.join(settings.MEDIA_ROOT, 'communities', 'posts', str(kwargs['post_pk']))
        post.delete()
        if os.path.exists(media_dir):
            try: os.rmdir(media_dir)
            except: pass
        return redirect('communities:post_list')
   
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'communities/post_update.html'
    pk_url_kwarg = 'post_pk'


    def test_func(self):
        review = Post.objects.get(pk=self.kwargs['post_pk'])
        user = self.request.user
        return (review.user == user) or user.is_superuser or user.is_staff


    def get(self, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_pk'])
        form = PostForm(instance=post)
        imageupdateformset = ImageUpdateFormSet(instance=post)
        imageaddform = ImageForm()
        return self.render_to_response({
            'post': post,
            'form': form,
            'imageupdateformset': imageupdateformset,
            'imageaddform': imageaddform,
        })


    def post(self, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_pk'])
        images = post.images.all()
        form = PostForm(self.request.POST, instance=post)
        imageformset = ImageUpdateFormSet(self.request.POST, self.request.FILES, queryset=images, instance=post)
        new_images = self.request.FILES.getlist('image')
        image_num = int(self.request.POST.get('images-TOTAL_FORMS'))

        if form.is_valid() and imageformset.is_valid():
            updated_post = form.save()
            
            for i in range(image_num):
                if self.request.POST.get(f'images-{i}-DELETE') == 'on':
                    target = Image.objects.get(pk=int(self.request.POST.get(f'images-{i}-id')))
                    target.delete()
                elif self.request.FILES.get(f'images-{i}-image'):
                    target = Image.objects.get(pk=int(self.request.POST.get(f'images-{i}-id')))
                    target.image = self.request.FILES.get(f'images-{i}-image')
                    target.save()

            for new_image in new_images:
                Image.objects.create(post=updated_post, image=new_image)

            return redirect('communities:detail', post.pk)

        return self.render_to_response({
            'form': form,
            'imageformset': imageformset,
        })


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


@receiver(post_delete, sender=Image)
def delete_post_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Image)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_image = instance.__class__.objects.get(pk=instance.pk).image.path
        try:
            new_image = instance.image.path
        except:
            new_image = None
        if new_image != old_image:
            if os.path.exists(old_image):
                os.remove(old_image)
    except:
        pass