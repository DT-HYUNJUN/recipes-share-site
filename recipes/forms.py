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
        fields = '__all__'


class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ('content',)