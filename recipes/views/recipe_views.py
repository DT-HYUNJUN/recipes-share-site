import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from recipes.forms import *
from recipes.models import *
from accounts.models import *
from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 12
    template_name = 'recipes/recipe_list.html'


    def get_context_data(self, **kwargs):
        context = dict()
        category = self.request.GET.get('filter')
        queryset = self.get_queryset()
        sort_param = self.request.GET.get('sort')
        if category:
            queryset = queryset.filter(category=category)
        
        if sort_param == 'created_at':
            queryset = queryset.order_by('-created_at')
        elif sort_param == 'difficulty':
            queryset = queryset.order_by('difficulty')
        elif sort_param == 'time':
            queryset = queryset.order_by('time')
        elif sort_param == 'likes':
            queryset = queryset.annotate(num_likes=Count('like_recipes')).order_by('-num_likes')
    
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
        context = super().get_context_data()
        recipe = context['recipe']
        prev_recipes = Recipe.objects.filter(pk__lt=recipe.pk).order_by('-pk')[:2]
        next_recipes = Recipe.objects.filter(pk__gt=recipe.pk).order_by('pk')[:2]
        adj_recipes = list(prev_recipes) + list(next_recipes)
        ingredients = RecipeIngredient.objects.select_related('ingredient').filter(recipe=recipe)
        steps = RecipeStep.objects.filter(recipe=recipe)
        reviews = recipe.recipes.prefetch_related('user').all()
        context['reviews'] = reviews
        context['review_form'] = RecipeReviewForm()
        context['adj_recipes'] = adj_recipes
        context['ingredients'] = ingredients
        context['steps'] = steps
        return context


class RecipeCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/recipe_create.html'

    
    def get(self, *args, **kwargs):
        ingredients = Ingredient.objects.all()
        options = [ingredient for ingredient in ingredients]
        ingredientformset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
        stepformset = RecipeStepFormSet(queryset=RecipeStep.objects.none())
        form = RecipeForm()
        equipform = EquipForm()
        return self.render_to_response({
            'form': form,
            'equipform': equipform,
            'ingredientformset': ingredientformset,
            'stepformset': stepformset,
            'options': options,
        })


    def post(self, *args, **kwargs):
        form = RecipeForm(self.request.POST, self.request.FILES)
        equipform = EquipForm(self.request.POST)
        stepforms = RecipeStepFormSet(self.request.POST)
        ingredientforms = RecipeIngredientFormSet(self.request.POST)
        ingredient_num = int(self.request.POST.get('recipeingredient_set-TOTAL_FORMS'))

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            if equipform.is_valid():
                equip = equipform.save(commit=False)
                equip.recipe = recipe
                equip.save()

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


class RecipeUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'recipes/recipe_update.html'
    pk_url_kwarg = 'recipe_pk'


    def test_func(self):
        keys = self.request.path.split('/')
        recipe = Recipe.objects.get(pk=int(keys[2]))
        isAuthor = self.request.user == recipe.user
        isAdmin = self.request.user.is_superuser or self.request.user.is_staff
        return isAuthor or isAdmin


    def get(self, *args, **kwargs):
        recipe = Recipe.objects.get(pk=kwargs['recipe_pk'])
        equip = Equip.objects.get(recipe=recipe)
        temp = RecipeIngredient.objects.filter(recipe=recipe)
        ingredients = Ingredient.objects.exclude(recipeingredient__in=temp)
        options = [ingredient for ingredient in ingredients]
        ingredientupdateformset = RecipeIngredientUpdateFormSet(instance=recipe, prefix='ingredient-update')
        ingredientformset = RecipeIngredientFormSet()
        stepupdateformset = RecipeStepUpdateFormSet(instance=recipe, prefix='step-update')
        stepformset = RecipeStepFormSet()
        form = RecipeUpdateForm(instance=recipe)
        equipform = EquipForm(instance=equip)
        return self.render_to_response({
            'form': form,
            'equipform': equipform,
            'ingredientupdateformset': ingredientupdateformset,
            'ingredientformset': ingredientformset,
            'stepupdateformset': stepupdateformset,
            'stepformset': stepformset,
            'options': options,
            'recipe': recipe,
        })


    def post(self, *args, **kwargs):
        recipe = Recipe.objects.get(pk=kwargs['recipe_pk'])
        ingredients = RecipeIngredient.objects.filter(recipe=recipe).order_by('pk')
        form = RecipeForm(self.request.POST, self.request.FILES, instance=recipe)
        equipform = EquipForm(self.request.POST, instance=recipe.equips)
        stepforms = RecipeStepFormSet(self.request.POST)
        stepupdateforms = RecipeStepUpdateFormSet(self.request.POST, prefix='step-update')
        ingredientforms = RecipeIngredientFormSet(self.request.POST)
        ingredientupdateforms = RecipeIngredientUpdateFormSet(self.request.POST, prefix='ingredient-update')
        update_ingredient_num = int(self.request.POST.get('ingredient-update-TOTAL_FORMS'))
        ingredient_num = int(self.request.POST.get('recipeingredient_set-TOTAL_FORMS'))
        step_num = int(self.request.POST.get('step-update-TOTAL_FORMS'))

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            if equipform.is_valid():
                equip = form.save(commit=False)
                equip.recipe = recipe
                equip.save()

            for subform in stepupdateforms:
                if subform.is_valid():
                    step = subform.save(commit=False)
                    if step.detail != '':
                        step.save()
                    else:
                        step.remove()

            for subform in stepforms:
                if subform.is_valid():
                    step = subform.save(commit=False)
                    if step.detail != '':
                        step.recipe = recipe
                        step.save()

            targets = list()

            for i in range(update_ingredient_num):
                ingredient_pk = self.request.POST.get(f'ingredient-update-{i}-ingredient')
                if ingredient_pk:
                    ingredient = Ingredient.objects.get(pk=ingredient_pk)
                    quantity = self.request.POST.get(f'ingredient-update-{i}-quantity')
                    RecipeIngredient(pk=ingredients[i].pk, recipe=recipe, ingredient=ingredient, quantity=quantity).save()
                else:
                    targets.append(ingredients[i].pk)
            
            for target in targets:
                RecipeIngredient.objects.get(pk=target).delete()

            raw_ingredient = list()

            for i in range(1, ingredient_num):
                raw_ingredient.append((self.request.POST.get(f'recipeingredient_set-{i}-ingredient'), self.request.POST.get(f'recipeingredient_set-{i}-quantity')))
            
            for ingredient, quantity in raw_ingredient:
                if ingredient.isdigit():
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=Ingredient.objects.get(pk=int(ingredient)), quantity=quantity)
                else:
                    temp = Ingredient.objects.create(name=ingredient)
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=temp, quantity=quantity)
            
            for i in range(step_num):
                if self.request.POST.get(f'step-update-{i}-DELETE') == 'on':
                    target = RecipeStep.objects.get(pk=self.request.POST.get(f'step-update-{i}-id'))
                    target.delete()

            return redirect('recipes:recipe_detail', recipe.pk)

        return self.render_to_response({'form': form, 'ingredientupdateforms': ingredientupdateforms, 'stepupdateforms': stepupdateforms, 'ingredientforms': ingredientforms, 'stepforms': stepforms,})


class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:recipe_list')
    pk_url_kwarg = 'recipe_pk'


    def test_func(self):
        recipe = Recipe.objects.get(pk=self.object.pk)
        return recipe.user == self.request.user or self.request.user.is_superuser or self.request.user.is_staff
    

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# class RecipeLikeView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         recipe_pk = kwargs['recipe_pk']
#         recipe = Recipe.objects.get(pk=recipe_pk)
#         if recipe.like_recipes.filter(pk=request.user.pk).exists():
#             recipe.like_recipes.remove(request.user)
#             like = False
#         else:
#             recipe.like_recipes.add(request.user)
#             like = True
#         context = {
#             'like': like,
#         }
#         return JsonResponse(context)

class RecipeLikeView(View):
    def post(self, request, recipe_pk):
        recipe = get_object_or_404(Recipe, pk=recipe_pk)

        if recipe.like_users.filter(pk=request.user.pk).exists():
            recipe.like_users.remove(request.user)
            is_liked = False
        else:
            recipe.like_users.add(request.user)
            is_liked = True

        context = {
            'is_liked': is_liked,
        }
        return JsonResponse(context)


class RecipeBookmarkView(View):
    def post(self, request, recipe_pk):
        recipe = get_object_or_404(Recipe, pk=recipe_pk)

        if recipe.bookmark_users.filter(pk=request.user.pk).exists():
            recipe.bookmark_users.remove(request.user)
            is_bookmark = False
        else:
            recipe.bookmark_users.add(request.user)
            is_bookmark = True

        context = {
            'is_bookmark': is_bookmark,
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


class RecipeFridge(ListView):
    model = Ingredient
    template_name = 'recipes/fridge.html'

    def get_queryset(self):
        user_ingredients = []
        user_ingredient_names = []
        total_recipes = []
        if self.request.user.is_authenticated:
            user_ingredients = UserIngredient.objects.filter(user=self.request.user)
            user_ingredient_names = user_ingredients.values_list('ingredient__name', flat=True)
            
            queryset = Recipe.objects.annotate(ingredient_count=Count('ingredients'))
            total_recipes = Recipe.objects.filter(ingredients__name__in=user_ingredient_names)
            total_recipes = total_recipes.distinct()
    
            return total_recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        already = []
        left = []
        user_ingredients = []
        user_ingredient_names = []
        total_recipes = []
        if self.request.user.is_authenticated:
            already = Ingredient.objects.filter(fridge_users=self.request.user)
            left = Ingredient.objects.exclude(fridge_users=self.request.user)
            user_ingredients = UserIngredient.objects.filter(user=self.request.user)
            user_ingredient_names = user_ingredients.values_list('ingredient__name', flat=True)
            total_recipes = self.get_queryset()  
        buttons = [x for x in range(len(already)+1, 10)]
   
        
        context.update({
            'already': already,
            'left': left,
            'buttons': buttons,
            'user_ingredients': user_ingredients, 
            'user_ingredients_names': user_ingredient_names,
            'total_recipes': total_recipes,
            
        })
        return context



    def post(self, request, *args, **kwargs):
        jsonObject = json.loads(request.body)
        target_name = jsonObject.get('target')
        ingredient = Ingredient.objects.get(name=target_name)
        user = request.user
        target = UserIngredient.objects.filter(ingredient=ingredient, user=user)

        try:
            if target:
                target.delete()
            else:
                UserIngredient.objects.create(ingredient=ingredient, user=user)
            return JsonResponse({'msg': 'success!'})
        except:
            return JsonResponse({'msg': 'error!'})


class RecipeEquip(ListView):
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