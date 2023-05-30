from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, View
from recipes.forms import RecipeForm, RecipeReviewForm, RecipeIngredientFormSet
from recipes.models import *


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 12
    # paginate_orphans = 3
    template_name = 'recipes/recipe_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(RecipeListView, self).get_context_data()
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        context['pagelist'] = pagelist
        return context


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


class RecipeCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/recipe_create.html'

    
    def get(self, *args, **kwargs):
        formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
        form = RecipeForm()
        return self.render_to_response({'form': form, 'formset': formset})


    def post(self, *args, **kwargs):
        formset = RecipeIngredientFormSet(self.request.POST)
        form = RecipeForm(self.request.POST)

        if form.is_valid() and form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            for subform in formset:
                ingredient = subform.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()

            return redirect('recipes:recipe_detail', recipe_pk=recipe.pk)
        
        return self.render_to_response({'form': form, 'formset': formset})


class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:recipe_list')
    pk_url_kwarg = 'recipe_pk'


    def test_func(self):
        recipe = Recipe.objects.get(pk=self.object.pk)
        return recipe.user == self.request.user or self.request.user.is_superuser or self.request.user.is_staff
    

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
    

class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_search.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        context['keyword'] = keyword
        return context

class RecipeFridge(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'recipes/fridge.html'
    
    def get_context_data(self, **kwargs):
        context = super(RecipeFridge, self).get_context_data()
        return context

