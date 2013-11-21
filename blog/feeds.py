from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from .models import Post, Category


class LatestFeed(Feed):
    def title(self):
        site = Site.objects.get_current()
        return '{0} latest feed'.format(site.name)

    def description(self):
        site = Site.objects.get_current()
        return '{0} latest posts feed.'.format(site.name)

    def link(self):
        return reverse('blog:index')

    def items(self):
        return Post.objects.published()[:10]

    def item_pubdate(self, obj):
        return obj.publish


class CategoryFeed(Feed):
    def get_object(self, request, slugs):
        try:
            return Category.objects.get_by_slugs(slugs)
        except (Category.DoesNotExist, Category.MultipleObjectsReturned):
            raise ObjectDoesNotExist

    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        return "{0} feed.".format(obj.title)

    def description(self, obj):
        return "Posts categorized as {0}.".format(obj.title.lower())

    def items(self, obj):
        descendants = obj.get_descendants(include_self=True)
        return Post.objects.get_from_categories(descendants)[:10]

    def item_pubdate(self, obj):
        return obj.publish
