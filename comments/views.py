from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from blog.models import Post
from .models import Comment, HierComment
from .forms import CommentForm, HierCommentForm


def post_comment(request, year, month, day, post):
    '''post comment'''
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of comments of this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # 提交表单
        comment_form = CommentForm(data=request.POST)
        # 检查form合法性
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # 生成实例，还未保存评论数据到数据库
            new_comment.post = post  # 关联
            new_comment.save()  # 保存
            return redirect(post)
    else:
        comment_form = CommentForm()
        return redirect(post)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


# hiercomment view
@require_POST
def submit_comment(request, year, month, day, post):
    new_comment = None
    form = HierCommentForm(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        # print('success')
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.user_name = request.user.username
        new_comment.save()
        location = "#c" + str(new_comment.id)
        return JsonResponse({'msg': 'success!', 'new_comment': location})
    return JsonResponse({'msg': '评论出错!'})
