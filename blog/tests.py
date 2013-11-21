import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Post, Category


class BlogTestCase(TestCase):
    def setUp(self):
        self.category = Category(title='Django', slug='django')
        self.category.save()
        self.category2 = Category(title='Rails', slug='rails',
                                  parent=self.category)
        self.category2.save()

        self.post = Post(title='DJ Ango', slug='django',
                         body='Yo DJ! Turn that music up!', status=2,
                         publish=datetime.datetime(2008, 5, 5, 16, 20))
        self.post.save()

        self.post2 = Post(title='Where my grails at?', slug='where',
                          body='I Can haz Holy plez?', status=2,
                          publish=datetime.datetime(2008, 4, 2, 11, 11))
        self.post2.save()

        self.post.categories.add(self.category)
        self.post2.categories.add(self.category2)

    def test_index(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertEqual(response.context['object_list'][0].title, 'DJ Ango')

    def test_category_page(self):
        response = self.client.get(self.category2.get_absolute_url())
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0].title,
                         'Where my grails at?')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.category2.get_feed_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.context['object'].title, 'DJ Ango')
        self.assertEqual(response.status_code, 200)
