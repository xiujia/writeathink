from django.shortcuts import render
from .forms import UserDetailForm
from django.contrib.auth.decorators import login_required


# 使用login_required装饰器，用户只有登录了才能访问其用户资料
@login_required
def account_profile(request):
    messages = []
    # post请求 表明是在修改用户资料
    if request.method == 'POST':
        # 使用getattr可以获得一个querydict，里面包含提交的内容
        # request_dic = getattr(request, 'POST')
        # print(request_dic)
        # print(request.FILES)
        form = UserDetailForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            messages.append('资料修改成功！')
    # 如果是get请求，则使用user生成表单
    form = UserDetailForm(instance=request.user)
    return render(request, 'account/user_detail.html',
                  context={'form': form,
                           'messages': messages, })
