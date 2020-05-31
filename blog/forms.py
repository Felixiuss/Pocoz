from django import forms

from blog.models import Comment


class EmailPostForm(forms.Form):
    """форма для отправки email"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """Форма создания комментария"""
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
