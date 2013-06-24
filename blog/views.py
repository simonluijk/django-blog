from django.http import Http404
from django.views.generic import DetailView, ListView
from blog.models import Post, Category


class PostDetailView(DetailView):
    """ Post detail """
    queryset = Post.objects.published()


class PostListView(ListView):
    """ List posts """
    paginate_by = 10
    paginate_orphans = 4
    queryset = Post.objects.published()


class CategoryPostListView(ListView):
    """ List posts in a category """
    paginate_by = 10
    template_name = 'blog/category_detail.html'

    def get_queryset(self):
        try:
            slugs = self.kwargs['slugs'].split('/')
            self.category = Category.objects.get_by_slug_list(slugs)
        except Category.DoesNotExist:
            raise Http404
        descendants = self.category.get_descendants(include_self=True)
        return Post.objects.get_from_categories(descendants)

    def get_context_data(self, *args, **kwargs):
        ctx = super(CategoryPostListView, self).get_context_data(*args, **kwargs)
        ctx['category'] = self.category
        return ctx
