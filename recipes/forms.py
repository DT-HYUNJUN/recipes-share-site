from django import forms
from .models import *


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeForm(forms.ModelForm):
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), input_formats='%H:%M')
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = '__all__'