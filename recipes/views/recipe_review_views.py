import json
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView, UpdateView
from recipes.models import *
from recipes.forms import *


class RecipeReviewCreateView(LoginRequiredMixin, CreateView):
    model = RecipeReview
    form_class = RecipeReviewForm
    template_name = 'recipes/review_create.html'


    def get_success_url(self):
        return reverse('recipes:recipe_detail', args=(self.object.recipe.pk,))
    

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            recipe_pk = kwargs['recipe_pk']
            recipe = Recipe.objects.get(pk=recipe_pk)
            review = form.save(commit=False)
            review.user = request.user
            review.recipe = recipe
            review.save()
            context = {
                'username': review.user.username,
                'content': review.content,
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'message': 'error',}, status=400)


class RecipeReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipeReview
    template_name = 'recipes/recipe_detail.html'
    pk_url_kwarg = 'review_pk'


    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        review_pk = jsonObject.get('pk')
        content = jsonObject.get('content')
        review = RecipeReview.objects.get(pk=review_pk)

        if review.user == request.user:
            if review is not None:
                review.update(content=jsonObject.get('content'))
                context = {
                    'content': content
                }
                return JsonResponse(context)
            return JsonResponse({'result': 'error!'}, status=400)
        else:
            raise PermissionDenied()


class RecipeReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RecipeReview
    template_name = 'recipes/recipe_detail.html'
    pk_url_kwarg = 'review_pk'


    def test_func(self):
        review = RecipeReview.objects.get(pk=self.kwargs['review_pk'])
        return self.request.user == review.user
    

    def get_success_url(self):
        recipe_pk = self.kwargs['recipe_pk']
        return reverse_lazy('recipes:recipe_detail', kwargs={'recipe_pk': recipe_pk})