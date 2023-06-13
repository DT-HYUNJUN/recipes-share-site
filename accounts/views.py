from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from communities.models import Post, Comment
from recipes.models import Recipe
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, PasswordChangeForm
# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            prev_url = request.session.get('prev_url')
            if prev_url:
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
        request.session['prev_url'] = request.META.get('HTTP_REFERER')

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')

    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=request.user.username)
    else:
        initial_data = {'birthdate': request.user.birthdate.strftime('%Y-%m-%d')} if request.user.birthdate else None
        form = CustomUserChangeForm(instance=request.user, initial=initial_data)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('index')


@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user
    if you == me:
        return redirect('accounts:profile', me.username)
    
    if me in you.followers.all():
        you.followers.remove(me)
    else:
        you.followers.add(me)

    return redirect('accounts:profile', you.username)

@login_required
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    post_list = Post.objects.filter(user=person).order_by('-pk')
    comment_list = Comment.objects.filter(user=person).order_by('-pk')
    recipe_list = Recipe.objects.filter(user=person).order_by('-pk')

    recipes = person.recipe_written.all()
    like_recipes = person.like_recipes.all()
    bookmark_recipes = person.bookmark_recipes.all()
    
    q = request.GET.get('q')

    paginator_post = Paginator(post_list, 5)
    post_page = request.GET.get('post_page')
    posts = paginator_post.get_page(post_page)
    
    paginator_comment = Paginator(comment_list, 5)
    comment_page = request.GET.get('comment_page')
    comments = paginator_comment.get_page(comment_page)

    paginator_recipe = Paginator(recipe_list, 5)
    recipe_page = request.GET.get('recipe_page')
    recipes = paginator_recipe.get_page(recipe_page)
    
    posts.q = q
    comments.q = q
    context = {
        'posts': posts,
        'comments': comments,
        'q': q,
        'person': person,
        'recipes': recipes,
        'like_recipes': like_recipes,
        'bookmark_recipes': bookmark_recipes,
    }
    return render(request, 'accounts/profile.html', context)