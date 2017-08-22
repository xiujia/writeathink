'''Comments model'''
from django.db import models
from django.conf import settings
from mptt.models import TreeForeignKey, MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField


class HierComment(MPTTModel):
    '''层级回复评论'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    post = models.ForeignKey(settings.COMMENT_ENTRY_MODEL,
                             verbose_name='文章', related_name='hiercomments')
    parent = TreeForeignKey(
        'self', blank=True, null=True, verbose_name='父级评论')
    content = RichTextUploadingField(verbose_name='评论', config_name='comment')
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    class MPTTMeta:
        order_insertion_by = ['-submit_date']

    def __str__(self):
        if self.parent is not None:
            return '%s 回复 %s' % (self.user_name, self.parent.user_name)
        return '%s 评论文章 post_%s' % (self.user_name, str(self.post.id))


# simple comment
class Comment(models.Model):
    '''commont model'''
    post = models.ForeignKey('blog.Post', related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'comment by {} on {}'.format(self.name, self.post)
