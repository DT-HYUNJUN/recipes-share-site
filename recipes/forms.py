from django import forms
from .models import *


class DifficultyWidget(forms.widgets.Widget):
    template_name = 'recipes/difficulty.html'  # 커스텀 위젯의 HTML 템플릿 경로


class DifficultyField(forms.CharField):
    widget = DifficultyWidget  # 위젯에 커스텀 위젯을 지정


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        label='요리 이름',
        widget=forms.TextInput(attrs={
            'pattern': '.{1,}',
            'required': 'true',
            'class': 'invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        })
    )
    content = forms.CharField(
        label='설명',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'pattern': '.{1,}',
            'required': 'true',
            'class': 'invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        }),
    )
    category = forms.CharField(
        label='카테고리',
    )
    time = forms.CharField(
        label='소요 시간(분)',
        widget=forms.TextInput(attrs={
            'pattern': '^[0-9]*$',
            'required': 'true',
            'class': 'invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        })
    )
    difficulty = DifficultyField(label='난이도')
    image = forms.ImageField(
        label='사진',
        widget=forms.FileInput(attrs={
            'class': 'border border-inherit'
        })
    )


    class Meta:
        model = Recipe
        fields = ('title', 'content', 'category', 'time', 'difficulty', 'image',)


class RecipeUpdateForm(forms.ModelForm):
    title = forms.CharField(
        label='요리 이름',
        widget=forms.TextInput(attrs={
            'pattern': '.{1,}',
            'required': 'true',
            'class': 'invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        })
    )
    content = forms.CharField(
        label='설명',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'pattern': '.{1,}',
            'required': 'true',
            'class': 'invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        }),
    )
    category = forms.CharField(
        label='카테고리',
    )
    time = forms.CharField(
        label='소요 시간(분)',
        widget=forms.TextInput(attrs={
            'pattern': '^[0-9]*$',
            'required': 'true',
            'class': 'invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        })
    )
    difficulty = DifficultyField(label='난이도')
    image = forms.ImageField(
        label='사진',
        widget=forms.ClearableFileInput(attrs={
            'class': 'border border-inherit',
            'can_delete': False
        }),
    )


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


RecipeIngredientUpdateFormSet = forms.inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=('ingredient', 'quantity',),
    extra=0,
    can_delete=True,
    labels={'ingredient': '', 'quantity': ''},
)


RecipeStepFormSet = forms.inlineformset_factory(
    Recipe,
    RecipeStep,
    fields=('detail',),
    extra = 1,
    can_delete=False,
    labels={'detail': ''},
    widgets={'detail': forms.Textarea(attrs={'rows': 1,})},
)


RecipeStepUpdateFormSet = forms.inlineformset_factory(
    Recipe,
    RecipeStep,
    fields=('detail',),
    extra=0,
    can_delete=True,
    labels={'detail': ''},
    widgets={'detail': forms.Textarea(attrs={'rows': 1,})},
)