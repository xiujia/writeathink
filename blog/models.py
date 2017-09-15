from django.db import models
from django.utils import timezone
# from user.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class PublishedManager(models.Manager):
    '''应用的管理器'''

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250, verbose_name='文章标题')
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', verbose_name='文章标识')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='blog_posts', verbose_name='文章作者')
    # body = models.TextField()
    # 正文使用ckeditor
    body = RichTextUploadingField(verbose_name='正文')
    publish = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    category = models.ForeignKey(Category)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', verbose_name='发布状态')
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # The Dahl-specific manager
    tags = TaggableManager()  # django-taggit 提供的tag管理器

    def get_absolute_url(self):
        '''
        我们通过使用strftime()方法来保证个位数的月份和日期
        需要带上0来构建URL（也就是01,02,03）
        '''
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    class Meta:
        verbose_name = '文章'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def increase_views(self):
        """阅读量"""
        self.views += 1
        self.save(update_fields=['views'])
