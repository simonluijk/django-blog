from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from blog.models import Post, Category


class BlogPostsFeed(Feed):
    _site = Site.objects.get_current()
    title = '%s feed' % _site.name
    description = '%s posts feed.' % _site.name

    def link(self):
        return reverse('blog_index')

    def items(self):
        return Post.objects.published()[:10]

    def item_pubdate(self, obj):
        return obj.publish


class BlogPostsByCategoryFeed(Feed):
    _site = Site.objects.get_current()
    title = '%s posts category feed' % _site.name
    
    def get_object(self, bits):
        try:
            return Category.objects.get_by_slug_list(bits)
        except (Category.DoesNotExist, Category.MultipleObjectsReturned):
            raise ObjectDoesNotExist

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Posts recently categorized as %s" % obj.title

    def items(self, obj):
        descendants = obj.get_descendants(include_self=True)
        return Post.objects.get_from_categories(descendants)[:10]
