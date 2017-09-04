from django.forms import ModelForm
from .models import User


class UserDetailForm(ModelForm):
    """用户详情页表单"""
    class Meta:
        # 关联的数据库模型
        model = User
        # 前端显示、可以修改的字段
        fields = ('nickname', 'qq', 'url', 'avatar')
