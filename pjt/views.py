import datetime, random
from django.db.models import Count
from django.shortcuts import render
from accounts.models import User
from recipes.models import Recipe


def index(request):
    like_recipes = Recipe.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:4]
    like_recipe1 = like_recipes[0]
    like_recipe2 = like_recipes[1]
    like_recipe3 = like_recipes[2]
    like_recipe4 = like_recipes[3]

    all_recipes = list(set(Recipe.objects.all()))
    random.shuffle(all_recipes)
    random_recipes = all_recipes[:4]

    recipes = Recipe.objects.all()
    recipes1 = Recipe.objects.all()[:4]
    recipes2 = Recipe.objects.all()[4:8]
    recipes3 = Recipe.objects.all()[8:12]

    today = datetime.date.today()
    users_with_birthday = User.objects.filter(username = request.user, birthdate__day=today.day, birthdate__month=today.month)
    is_birthday = 1 if users_with_birthday.exists() else 0

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
        'is_birthday' : is_birthday,
    }
    
    return render(request, 'index.html', context)


def BadRequestView(request, exception):
    return render(request, '400.html', status=403)


def ForbiddenView(request, exception):
    return render(request, '403.html', status=403)


def NotFoundView(request, exception):
    return render(request, '404.html', status=404)


def ServerErrorView(request):
    return render(request, '500.html', status=500)