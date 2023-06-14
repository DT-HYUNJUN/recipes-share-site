from django import forms
from django.forms import inlineformset_factory
from .models import *


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목을 입력해 주세요.'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용을 입력해 주세요.'
            }
        )
    )


    class Meta:
        model = Post
        fields = ('title', 'content',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].label = '제목'
        self.fields['content'].label = '내용'

        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea
    )


    class Meta:
        model = Comment
        fields = ('content',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={'multiple': True})
    )


    class Meta:
        model = Image
        fields = ('image',)


class ImageUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        label='',
        widget=forms.ClearableFileInput
    )


    class Meta:
        model = Image
        fields = ('image',)


ImageFormSet = inlineformset_factory(
    Post,
    Image,
    fields=('image',),
    form=ImageForm,
    extra=0,
)


ImageUpdateFormSet = inlineformset_factory(
    Post,
    Image,
    fields=('image',),
    form=ImageUpdateForm,
    extra=0,
    can_delete=True,
)