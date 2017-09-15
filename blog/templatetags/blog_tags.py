# -*- coding:utf-8 -*-
'''simple_tag '''


from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from taggit.models import Tag
from ..models import Post, Category


register = template.Library()


@register.simple_tag
def total_posts():
    '''返回总数'''
    return Post.published.count()


@register.simple_tag
def all_posts():
    """所有文章"""
    return Post.published.all()


@register.simple_tag
def get_categories():
    """分类目录"""
    return Category.objects.annotate(
        num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    """获取标签"""
    return Tag.objects.annotate(
        num_posts=Count('post')).filter(num_posts__gt=0)


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    '''最新文章的渲染模板'''
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.assignment_tag
def get_most_commented_posts(count=5):
    '''返回评论最多的帖子'''
    return Post.published.annotate(
        total_comments=Count('hiercomments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    '''markdown filter'''
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_archives():
    """归档"""
    # return Post.objects.dates('created_time','month',order='DESC')
    # from django.db import connections
    # from django.db.models import Count
    # Post.objects.extra(select={'month': connections[Post.objects.db].ops.date_trunc_sql('month', 'pub_date')}).values('month').annotate(dcount=Count('pub_date'))

    post_list = Post.objects.all()
    year_month = set()
    for post in post_list:
        # 把每篇文章的年、月以元组形式添加到集合中
        year_month.add((post.publish.year, post.publish.month))
    post_counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
    for post in post_list:
        # 按年月统计post数目
        post_counter[(post.publish.year, post.publish.month)] += 1
    year_month_counter = []
    for key in post_counter:
        year_month_counter.append([key[0], key[1], post_counter[key]])
    year_month_counter.sort(reverse=True)
    date_dict_list = []
    for year, month, counter in year_month_counter:
        date = {}
        date['year'] = year
        date['month'] = month
        date['num'] = counter
        date_dict_list.append(date)
    return date_dict_list
