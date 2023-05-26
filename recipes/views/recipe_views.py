from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View
from recipes.forms import RecipeReviewForm
from recipes.models import *


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    pk_url_kwarg = 'recipe_pk'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = Recipe.objects.get(pk=self.object.pk)
        reviews = recipe.recipes.all()
        context['reviews'] = reviews
        context['review_form'] = RecipeReviewForm()
        return context


class RecipeCreateView(CreateView):
    model = Recipe
    fields = ('title', 'category', 'time', 'difficulty', 'content', 'image', 'ingredients',)
    template_name = 'recipes/recipe_create.html'


class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:recipe_list')
    pk_url_kwarg = 'recipe_pk'


    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RecipeLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipe_pk = kwargs['recipe_pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        if recipe.like_recipes.filter(pk=request.user.pk).exists():
            recipe.like_recipes.remove(request.user)
            like = False
        else:
            recipe.like_recipes.add(request.user)
            like = True
        context = {
            'like': like,
        }
        return JsonResponse(context)


class RecipeBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipe_pk = kwargs['recipe_pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        if recipe.bookmark.filter(pk=request.user.pk).exists():
            recipe.bookmark.remove(request.user)
            bookmark = False
        else:
            recipe.bookmark.add(request.user)
            bookmark = True
        context = {
            'bookmark': bookmark,
        }
        return JsonResponse(context)