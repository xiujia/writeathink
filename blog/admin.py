'''Register your models here.'''
from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    '''定制展示形式 '''
    list_display = ('title', 'slug', 'author', 'publish', 'category', 'status')
    list_filter = ('status', 'created', 'publish', 'author', 'category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
