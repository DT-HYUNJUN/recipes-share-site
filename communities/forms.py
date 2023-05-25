from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].label = '제목'
        self.fields['content'].label = '내용'

        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['content'].label = '댓글 내용'