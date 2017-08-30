'''Create your views here. '''
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from haystack.query import SearchQuerySet
from .models import Post, Category
from .forms import EmailPostForm, SearchForm


def site_index(request):
    '''site index page '''
    posts = Post.objects.all()
    return render(request,
                  'blog/post/index.html', context={'post_list': posts})


def post_list(request, tag_slug=None):
    '''获取post列表'''
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer ,deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # out of range, deliver last page
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'page': page,
                   'tag': tag})


class PostListView(ListView):
    '''类视图'''
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3


def post_category(request, cate_name):
    """分类视图"""
    cate = get_object_or_404(Category, name=cate_name)
    postcate_list = Post.published.filter(category=cate)
    return render(request,
                  'blog/post/list.html',
                  context={'posts': postcate_list})


def post_archives(request, year, month):
    """归档视图"""
    dates = Post.published.filter(publish__year=year,
                                  publish__month=month,
                                  ).order_by('-publish')
    return render(request,
                  'blog/post/list.html',
                  context={'posts': dates})


def post_detail(request, year, month, day, post):
    '''post详情页'''
    post = get_object_or_404(
        Post, slug=post, status='published',
        publish__year=year, publish__month=month,
        publish__day=day)
    post.increase_views()  # 阅读量+1
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]
    return render(
        request, 'blog/post/detail.html',
        {'post': post,
         'similar_posts': similar_posts})


def post_share(request, post_id):
    '''分享post'''
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    clean_data = None
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                clean_data['name'], clean_data['email'], post.title)
            message = 'Read "{}" at {} \n\n{}\'s comments: {}'.format(
                post.title, post_url,
                clean_data['name'],
                clean_data['comments'])
            send_mail(subject, message, 'admin@myblog.com', [clean_data['to']])
            sent = True
    else:  # get请求得到一个空的表单
        form = EmailPostForm()
    return render(request,
                  'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent,
                   'cd': clean_data})


def post_search(request):
    # post search
    form = SearchForm()
    clean_data = None
    results = None
    total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            clean_data = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(
                text=clean_data['query']).load_all()
            total_results = results.count()

    return render(request, 'blog/post/search.html',
                  {'form': form,
                   'cd': clean_data,
                   'results': results,
                   'total_results': total_results})
