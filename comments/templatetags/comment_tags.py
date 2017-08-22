'''comment tags'''
from django import template
from django.conf import settings
from django.apps import apps
from django.db.models.aggregates import Count
from ..forms import HierCommentForm

register = template.Library()


@register.simple_tag
def generate_form_for(post):
    form = HierCommentForm(initial={'post': post.id})
    return form


@register.simple_tag
def get_comment_list_of(post):
    return post.hiercomments.all


@register.simple_tag
def get_comments_user_count(post):
    user_list = []
    comments = post.hiercomments.all()
    for comment in comments:
        if comment.user not in user_list:
            user_list.append(comment.user)
    return len(user_list)
