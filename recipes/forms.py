from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Field)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'content', 'category', 'time', 'difficulty', 'image',)


class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ('content',)


RecipeIngredientFormSet = forms.inlineformset_factory(Recipe, RecipeIngredient, fields=('ingredient', 'quantity',), extra=1, can_delete=False)