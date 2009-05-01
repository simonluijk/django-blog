from datetime import date, datetime
from django.db.models import Manager


class PostManager(Manager):
    def published(self):
        """
        Return published posts that are not in the future.
        """
        today = date.today()
        today_end = datetime(today.year, today.month, today.day, 23, 59, 59)
        return self.get_query_set().filter(status__gte=2, publish__lte=today_end)


    def get_from_categories(self, categories):
        """
        Return publish posts in supplied categories
        """
        return self.published().filter(categories__in=categories).distinct()


class CategoryManager(Manager):
    def get_by_slug_list(self, slugs):
        """
        Get category from slug list
        """
        tmp_key = ''
        kwargs = {}
        for slug in reversed(slugs):
            key = '%s%s' % (tmp_key, 'slug')
            kwargs[str(key)] = str(slug)
            if tmp_key:
                tmp_key = '%s%s__' % (tmp_key, 'parent')
            else:
                tmp_key = 'parent__'

        category = self.get_query_set().filter(**kwargs).get()
        if not category.is_root_node() and len(slugs) is 1:
            raise self.model.DoesNotExist

        return category
