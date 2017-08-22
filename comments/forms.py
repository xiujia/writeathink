'''comment form'''
from django import forms
from .models import Comment, HierComment


class CommentForm(forms.ModelForm):
    '''comment form'''
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class HierCommentForm(forms.ModelForm):
    '''HierComment form'''
    honeypot = forms.CharField(required=False,
                               label='If you enter anything in this field,\
                               your comment will be treated as spam!')

    class Meta:
        model = HierComment
        fields = ('content', 'parent', 'post')

    def clean_honeypot(self):
        '''验证honeypot字段，如果有输入，则是垃圾评论'''
        value = self.cleaned_data['honeypot']
        if value:
            return forms.ValidationError(self.fields['honeypot'].error_message)
        return value
