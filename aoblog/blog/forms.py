from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'share_post-name',
        'placeholder': 'Your name',
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'share_post-email',
        'placeholder': 'your@email.com',
    }))
    to = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'share_post-sentto',
        'placeholder': 'recipient@email.com',
    }))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'id': 'share_post-comment',
                                'placeholder': 'Your comment',
                               }))


class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control bg-white',
        'id': 'comment_input',
        'rows': '4',
        'maxlength': 255,
    }))
    class Meta:
        model = Comment
        fields = ['body']