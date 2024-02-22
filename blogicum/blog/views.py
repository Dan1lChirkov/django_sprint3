from django.shortcuts import render, get_object_or_404

from django.db.models.functions import Now

from django.db.models import Q

from blog.models import Post, Category

max_posts_num: int = 5

post_filter = {
    'is_published': True,
    'category__is_published': True
}


def index(request):
    tempalte = 'blog/index.html'
    posts = Post.objects.select_related(
        'category',
        'location'
    ).filter(
        **post_filter,
        pub_date__lte=Now(),
    ).order_by('-created_at')[:max_posts_num]
    context = {'posts': posts}
    return render(request, tempalte, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        Q(pk=id) & (Q(pub_date__lte=Now()) & Q(
            is_published=True) & Q(category__is_published=True))
    )
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
    posts = Post.objects.select_related(
        'category',
        'location'
    ).filter(
        **post_filter,
        category__slug=category_slug,
        pub_date__lte=Now(),
    )
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, template, context)
