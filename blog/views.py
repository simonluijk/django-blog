from django.http import Http404
from django.views.generic import list_detail
from blog.models import Post, Category


def post_list(request, page=0):
    return list_detail.object_list(request, queryset=Post.objects.published(),
                                   paginate_by=10, page=page)


def post_detail(request, slug):
    return list_detail.object_detail(request, queryset=Post.objects.published(),
                                     slug=slug)


def category(request, slugs):
    try:
        category = Category.objects.get_by_slug_list(slugs.split('/'))
    except Category.DoesNotExist:
        raise Http404
    descendants = category.get_descendants(include_self=True)
    queryset = Post.objects.get_from_categories(descendants)
    return list_detail.object_list(request, queryset=queryset,
                                   extra_context={'category': category},
                                   template_name='blog/category_detail.html')
