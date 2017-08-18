'''Comments model'''
from django.db import models


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
