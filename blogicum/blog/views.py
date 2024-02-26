from django.shortcuts import render, get_object_or_404

from django.db.models.functions import Now

from blog.models import Post, Category

MAX_POSTS_NUM: int = 5


def get_posts_qs():
    is_published: bool = True
    category_is_published: bool = True
    date_time_now = Now()
    return Post.objects.filter(
        is_published=is_published,
        category__is_published=category_is_published,
        pub_date__lte=date_time_now,
    )


def index(request):
    tempalte = 'blog/index.html'
    posts = get_posts_qs().order_by('-created_at')[:MAX_POSTS_NUM]
    context = {'posts': posts}
    return render(request, tempalte, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_posts_qs(),
        pk=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values(
            'title',
            'description'
        ),
        is_published=True,
        slug=category_slug)
    posts = get_posts_qs().filter(
        category__slug=category_slug,
    )
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, template, context)
