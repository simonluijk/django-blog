from django.db.models import Manager
from django.utils.timezone import now


class PostManager(Manager):
    def published(self):
        """
        Return published posts that are not in the future.
        """
        return self.get_query_set().filter(status=self.model.PUBLISHED,
                                           publish__lte=now())

    def get_from_categories(self, categories):
        """
        Return publish posts in supplied categories
        """
        return self.published().filter(categories__in=categories).distinct()


class CategoryManager(Manager):
    def get_by_slugs(self, slugs):
        """
        Get category from slug list
        """
        if isinstance(slugs, basestring):
            slugs = slugs.split('/')

        base_key = ''
        kwargs = {}
        for slug in reversed(slugs):
            if base_key:
                key = '{0}{1}'.format(base_key, 'slug')
                base_key = '{0}{1}__'.format(base_key, 'parent')
            else:
                key = 'slug'
                base_key = 'parent__'
            kwargs[str(key)] = str(slug)

        category = self.get_query_set().filter(**kwargs).get()
        if not category.is_root_node() and len(slugs) is 1:
            raise self.model.DoesNotExist
        return category
