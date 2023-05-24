from django.urls import path
from .views import *


app_name = 'recipes'
urlpatterns = [
    # 레시피
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:recipe_pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:recipe_pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
]
