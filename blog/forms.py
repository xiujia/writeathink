'''创建表单类'''
from django import forms


class EmailPostForm(forms.Form):
    '''通过Email分享帖子的表单'''
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    '''search form'''
    query = forms.CharField()