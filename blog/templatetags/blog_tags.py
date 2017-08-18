# -*- coding:utf-8 -*-
'''simple_tag '''


from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    '''返回总数'''
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    '''最新文章的渲染模板'''
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.assignment_tag
def get_most_commented_posts(count=5):
    '''返回评论最多的帖子'''
    return Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    '''markdown filter'''
    return mark_safe(markdown.markdown(text))