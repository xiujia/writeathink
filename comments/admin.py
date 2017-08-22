from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment, HierComment


class CommentAdmin(admin.ModelAdmin):
    '''管理评论'''
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)
admin.site.register(HierComment, MPTTModelAdmin)

