# -*- coding:utf-8 -*-
'''feed'''


from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    '''latest posts feed'''
    title = 'Write@Think'
    link = '/blog/'
    description = '最新文章-writeathink.cn'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
        