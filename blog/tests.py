"""
>>> from django.test import Client
>>> from blog.models import Post, Category
>>> import datetime
>>> from django.core.urlresolvers import reverse
>>> client = Client()

>>> category = Category(title='Django', slug='django')
>>> category.save()
>>> category2 = Category(title='Rails', slug='rails', parent=category)
>>> category2.save()

>>> post = Post(title='DJ Ango', slug='django', body='Yo DJ! Turn that music up!', status=2, publish=datetime.datetime(2008,5,5,16,20))
>>> post.save()

>>> post2 = Post(title='Where my grails at?', slug='where', body='I Can haz Holy plez?', status=2, publish=datetime.datetime(2008,4,2,11,11))
>>> post2.save()

>>> post.categories.add(category)
>>> post2.categories.add(category2)

>>> response = client.get(reverse('blog_index'))
>>> response.context['object_list']
[<Post: DJ Ango>, <Post: Where my grails at?>]
>>> response.status_code
200

>>> response = client.get(category2.get_absolute_url())
>>> response.context['object_list']
[<Post: Where my grails at?>]
>>> response.status_code
200

>>> response = client.get(post.get_absolute_url())
>>> response.context['object']
<Post: DJ Ango>
>>> response.status_code
200
"""
