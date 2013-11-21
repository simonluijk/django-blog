from django.http import Http404
from django.views.generic import ListView, DetailView
from blog.models import Post, Category


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        if 'slugs' in self.kwargs:
            try:
                category = Category.objects.get_by_slugs(self.kwargs['slugs'])
            except Category.DoesNotExist:
                raise Http404
            descendants = category.get_descendants(include_self=True)
            return Post.objects.get_from_categories(descendants)
        else:
            return Post.objects.published()


class PostDetailView(DetailView):
    queryset = Post.objects.published()
