from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    """拓展User模型"""
    nickname = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='昵称')
    qq = models.CharField(max_length=20, blank=True,
                          null=True, verbose_name='QQ号码')
    url = models.URLField(max_length=100, blank=True,
                          null=True, verbose_name='个人网页地址')
    avatar = ProcessedImageField(upload_to='avatar',
                                 default='avatar/default.png',
                                 verbose_name='头像',
                                 # 将图片处理成85x85的尺寸
                                 processors=[ResizeToFill(85, 85)])

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """复写是save方法，不同用户不同头像文件路径"""
        # 当用户更改头像的时候，avatar.name = '文件名'
        # 其他情况下avatar.name = 'upload_to/文件名'
        if len(self.avatar.name.split('/')) == 1:
            # print('before:%s' % self.avatar.name)
            # 用户上传图片时，将avatar.name改为 用户名/文件名
            self.avatar.name = self.username + '/' + self.avatar.name
        super(User, self).save()
        # 调用父类的save()方法后，avatar.name就变成了'upload_to/用户名/文件名'
        # print('after:%s' % self.avatar.name)
        # print('avatar_path: %s' % self.avatar.path)
