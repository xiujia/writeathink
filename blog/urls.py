"""urls"""
from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [
    # list
    url(r'^$', views.post_list, name='post_list'),
    # url(r'^$', views.PostListView.as_view(), name='post_list'),
    # pos_list_by_tag
    url(r'^tag(?P<tag_slug>[-\w]+)/$',
        views.post_list, name='post_list_by_tag'),
    # post_detail
    url(
        r"^(?P<year>\d{4})/(?P<month>\d{1,2})/("
        r"?P<day>\d{1,2})/(?P<post>[-\w]+)/$",
        views.post_detail, name='post_detail'),

    # category
    url(r'^category/(?P<cate_name>[-\w]+)/$',
        views.post_category, name='post_category'),
    # archive
    url(r'archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2}).$',
        views.post_archives, name='post_archives'),

    # post_share
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    # post_feed
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
    # post_search
    # url(r'^search/$', views.post_search, name='post_search'),
]
