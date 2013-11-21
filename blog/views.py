from django.http import Http404
from django.views.generic import ListView, DetailView
from blog.models import Post, Category


class PostListView(ListView):
    model = Post
    paginate_by = 10
    paginate_orphans = 4

    def get_queryset(self):
        try:
            self.category = Category.objects.get_by_slugs(self.kwargs['slugs'])
        except Category.DoesNotExist:
            raise Http404
        except KeyError:
            return Post.objects.published()
        else:
            descendants = self.category.get_descendants(include_self=True)
            return Post.objects.get_from_categories(descendants)

    def get_context_data(self, *args, **kwargs):
        ctx = super(PostListView, self).get_context_data(*args, **kwargs)
        try:
            ctx['category'] = self.category
        except AttributeError:
            pass
        return ctx


class PostDetailView(DetailView):
    queryset = Post.objects.published()
