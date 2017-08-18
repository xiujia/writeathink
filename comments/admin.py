from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    '''管理评论'''
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)

