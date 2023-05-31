from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Field)
from ckeditor_uploader.fields import RichTextUploadingFormField


class DifficultyWidget(forms.widgets.Widget):
    template_name = 'recipes/difficulty.html'  # 커스텀 위젯의 HTML 템플릿 경로


class DifficultyField(forms.CharField):
    widget = DifficultyWidget  # 위젯에 커스텀 위젯을 지정


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        label='요리 이름',
    )
    content = RichTextUploadingFormField(
        label='조리법',
    )
    category = forms.CharField(
        label='카테고리',
    )
    time = forms.CharField(
        label='소요 시간',
    )
    difficulty = DifficultyField(label='난이도')


    class Meta:
        model = Recipe
        fields = ('title', 'content', 'category', 'time', 'difficulty', 'image',)


class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ('content',)


RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=('ingredient', 'quantity',),
    extra=1,
    can_delete=False,
    labels={'ingredient': '', 'quantity': ''},
)