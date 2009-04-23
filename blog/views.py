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


def post_detail(request, slug, year, month):
    try:
        date = datetime.strptime('%d %s' % (int(year), month), '%Y %b')
    except ValueError:
        raise Http404
    return list_detail.object_detail(request,
        queryset = Post.objects.published().filter(publish__year=date.year, publish__month=date.month),
        slug = slug
    )


def category_list(request):
    return list_detail.object_list(request,
        queryset = Category.objects.all(),
        template_name = 'blog/category_list.html'
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug__iexact=slug)
    return list_detail.object_list(request,
        queryset = category.post_set.published(),
        extra_context = {'category': category},
        template_name = 'blog/category_detail.html'
    )
