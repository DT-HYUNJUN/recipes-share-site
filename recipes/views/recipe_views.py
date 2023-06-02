from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, View
from recipes.forms import RecipeForm, RecipeReviewForm, RecipeIngredientFormSet, RecipeStepFormset
from recipes.models import *
from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 12
    template_name = 'recipes/recipe_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('filter')
        queryset = self.get_queryset()
        if category:
            queryset = queryset.filter(category=category)
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page_obj'] = page
        context['pagelist'] = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        return context

    def get_queryset(self):
        return super().get_queryset()


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
        ingredients = Ingredient.objects.all()
        options = [ingredient for ingredient in ingredients]
        ingredientformset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
        stepformset = RecipeStepFormset(queryset=RecipeStep.objects.none())
        form = RecipeForm()
        return self.render_to_response({
            'form': form,
            'ingredientformset': ingredientformset,
            'stepformset': stepformset,
            'options': options,
        })


    def post(self, *args, **kwargs):
        # ingredients = Ingredient.objects.all()
        # formset = RecipeIngredientFormSet(self.request.POST)
        
        form = RecipeForm(self.request.POST, self.request.FILES)
        stepforms = RecipeStepFormset(self.request.POST)
        ingredientforms = RecipeIngredientFormSet(self.request.POST)
        # form = RecipeForm(self.request.POST)
        ingredient_num = int(self.request.POST.get('recipeingredient_set-TOTAL_FORMS'))

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            for subform in stepforms:
                if subform.is_valid():
                    step = subform.save(commit=False)
                    if step.detail != '':
                        step.recipe = recipe
                        step.save()
            
            raw_ingredient = list()

            for i in range(1, ingredient_num):
                raw_ingredient.append((self.request.POST.get(f'recipeingredient_set-{i}-ingredient'), self.request.POST.get(f'recipeingredient_set-{i}-quantity')))
            
            for ingredient, quantity in raw_ingredient:
                if ingredient.isdigit():
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=Ingredient.objects.get(pk=int(ingredient)), quantity=quantity)
                else:
                    temp = Ingredient.objects.create(name=ingredient)
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=temp, quantity=quantity)

            return redirect('recipes:recipe_detail', recipe_pk=recipe.pk)
        
        return self.render_to_response({'form': form, 'ingredientforms': ingredientforms, 'stepforms': stepforms,})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        
        # 제목에 키워드가 포함된 레시피들 쿼리셋
        title_queryset = self.model.objects.filter(title__icontains=keyword)
        
        # 재료에 키워드가 포함된 레시피들 쿼리셋
        ingredient_queryset = self.model.objects.filter(ingredients__name__icontains=keyword)
        
        context['keyword'] = keyword
        context['title_recipes'] = title_queryset
        context['ingredient_recipes'] = ingredient_queryset
        return context

      
class RecipeNameSearchView(RecipeSearchView):
    template_name = 'recipes/recipe_search_name.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        
        # 제목에 키워드가 포함된 레시피들 쿼리셋
        title_queryset = self.model.objects.filter(title__icontains=keyword).order_by('-created_at')
        
        sort_param = self.request.GET.get('sort')
        
        if sort_param == 'created_at':
            title_queryset = title_queryset.order_by('-created_at')
        elif sort_param == 'difficulty':
            title_queryset = title_queryset.order_by('difficulty')
        elif sort_param == 'time':
            title_queryset = title_queryset.order_by('time')
        elif sort_param == 'likes':
            title_queryset = title_queryset.annotate(num_likes=Count('like_recipes')).order_by('-num_likes')

        context['keyword'] = keyword
        context['title_recipes'] = title_queryset
        context['sort_param'] = sort_param
        return context

    
class RecipeIngredientSearchView(RecipeSearchView):
    template_name = 'recipes/recipe_search_ingredient.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        
        # 제목에 키워드가 포함된 레시피들 쿼리셋
        ingredient_queryset = self.model.objects.filter(ingredients__name__icontains=keyword)
        
        sort_param = self.request.GET.get('sort')
        
        if sort_param == 'created_at':
            ingredient_queryset = ingredient_queryset.order_by('-created_at')
        elif sort_param == 'difficulty':
            ingredient_queryset = ingredient_queryset.order_by('difficulty')
        elif sort_param == 'time':
            ingredient_queryset = ingredient_queryset.order_by('time')
        elif sort_param == 'likes':
            ingredient_queryset = ingredient_queryset.annotate(num_likes=Count('like_recipes')).order_by('-num_likes')

        context['keyword'] = keyword
        context['ingredient_queryset'] = ingredient_queryset
        context['sort_param'] = sort_param
        return context


class RecipeFridge(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'recipes/fridge.html'
    
    def get_context_data(self, **kwargs):
        context = super(RecipeFridge, self).get_context_data()
        return context


class RecipeEquip(LoginRequiredMixin, ListView):
    # model = Equip
    template_name = 'recipes/equip.html'
    model = Recipe
    paginate_by = 12
    # paginate_orphans = 3
    
    def get_context_data(self, **kwargs):
        context = super(RecipeEquip, self).get_context_data()
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        context['pagelist'] = pagelist
        return context
    
    # def get_context_data(self, **kwargs):
    #     context = super(RecipeFridge, self).get_context_data()
    #     return context