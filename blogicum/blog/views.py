from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

from django.db.models.functions import Now

from django.db.models import Q


def index(request):
    tempalte = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category',
        'location'
    ).filter(
        pub_date__lte=Now(),
        is_published=True,
        category__is_published=True
    ).order_by('-created_at')[:5]
    context = {'post_list': post_list}
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
    post_list = Post.objects.select_related(
        'category',
        'location'
    ).filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=Now(),
        category__is_published=True
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
