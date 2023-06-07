from django.shortcuts import render
from recipes.models import Recipe
from django.db.models import Count

def index(request):
    like_recipe1 = Recipe.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:1]
    like_recipe2 = Recipe.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[1:2]
    like_recipe3 = Recipe.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[2:3]
    like_recipe4 = Recipe.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[3:4]
    
    random_recipes = Recipe.objects.order_by('?')[:4]
    
    recipes = Recipe.objects.all()
    recipes1 = Recipe.objects.all()[:4]
    recipes2 = Recipe.objects.all()[4:8]
    recipes3 = Recipe.objects.all()[8:12]
    context = {
        'recipes': recipes,
        'recipes1': recipes1,
        'recipes2': recipes2,
        'recipes3': recipes3,
        'random_recipes': random_recipes,
        'like_recipe1': like_recipe1,
        'like_recipe2': like_recipe2,
        'like_recipe3': like_recipe3,
        'like_recipe4': like_recipe4,
    }
    return render(request, 'index.html', context)