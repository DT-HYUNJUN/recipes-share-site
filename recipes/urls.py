from django.urls import path
from .views import *


app_name = 'recipes'
urlpatterns = [
    # 레시피
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:recipe_pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:recipe_pk>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:recipe_pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('<int:recipe_pk>/like/', RecipeLikeView.as_view(), name='recipe_like'),
    path('<int:recipe_pk>/bookmark/', RecipeBookmarkView.as_view(), name='recipe_bookmark'),
    path('search/', RecipeSearchView.as_view(), name='recipe_search'),
    path('search/name/', RecipeNameSearchView.as_view(), name='recipe_search_name'),
    path('search/ingredient/', RecipeIngredientSearchView.as_view(), name='recipe_search_ingredient'),
    # 레시피 리뷰
    path('<int:recipe_pk>/create/', RecipeReviewCreateView.as_view(), name='review_create'),
    path('review_update/', RecipeReviewUpdateView.as_view(), name='review_update'),
    path('<int:recipe_pk>/<int:review_pk>/delete/', RecipeReviewDeleteView.as_view(), name='review_delete'),
    # 냉장고
    path('fridge/', RecipeFridge.as_view(), name='recipe_fridge'),
    # 도구
    path('equip/', RecipeEquip.as_view(), name='recipe_equip')
]
