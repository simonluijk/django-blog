from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import date_based, list_detail
from blog.models import Post, Category


def post_list(request, page=0):
    return list_detail.object_list(request,
        queryset = Post.objects.published(),
        paginate_by = 10,
        page = page
    )


def post_archive_year(request, year):
    return date_based.archive_year(request,
        queryset = Post.objects.published(),
        year = year,
        date_field = 'publish',
        make_object_list = True
    )


def post_archive_month(request, year, month):
    return date_based.archive_month(request,
        queryset = Post.objects.published(),
        year = year,
        month = month,
        date_field = 'publish'
    )


def post_detail(request, slug):
    return list_detail.object_detail(request,
        queryset = Post.objects.published(),
        slug = slug
    )


def category(request, slugs):
    try:
        category = Category.objects.get_by_slug_list(slugs.split('/'))
    except Category.DoesNotExist:
        raise Http404
    descendants = category.get_descendants(include_self=True)
    return list_detail.object_list(request,
        queryset = Post.objects.get_from_categories(descendants),
        extra_context = {'category': category},
        template_name = 'blog/category_detail.html'
    )
