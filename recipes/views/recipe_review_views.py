from typing import Optional
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from recipes.models import *
from recipes.forms import *


class RecipeReviewCreateView(LoginRequiredMixin, CreateView):
    model = RecipeReview
    form_class = RecipeReviewForm
    template_name = 'recipes/review_create.html'


    def get_success_url(self):
        return reverse('recipes:recipe_detail', args=(self.object.recipe.pk,))


class RecipeReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RecipeReview
    form_class = RecipeReviewForm
    template_name = 'recipes/review_update.html'
    pk_url_kwarg = 'review_pk'


    def test_func(self):
        review = RecipeReview.objects.get(pk=self.kwargs['review_pk'])
        user = self.request.user
        return (review.user == user) or user.is_superuser or user.is_staff


    def get_success_url(self):
        recipe_pk = self.kwargs['recipe_pk']
        return reverse_lazy('recipes:recipe_detail', kwargs={'recipe_pk': recipe_pk})


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