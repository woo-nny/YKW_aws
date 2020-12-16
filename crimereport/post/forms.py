from .models import Comment, Post
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = '댓글'

class writeForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text','photo']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
