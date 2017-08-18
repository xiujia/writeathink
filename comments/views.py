from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


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
