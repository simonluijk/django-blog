from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.syndication.views import feed
from blog import views as blog_views
from blog.feeds import BlogPostsFeed, BlogPostsByCategoryFeed

urlpatterns = patterns('',
    url(r'^$', blog_views.post_list, name='blog_index'),
    url(r'^topic/(?P<slugs>[-\w/]+)/$', blog_views.category, name='blog_category'),
    url(r'^feeds/(?P<url>.*)/$', feed, {
            'feed_dict': {
                'latest': BlogPostsFeed,
                'topic': BlogPostsByCategoryFeed,
            }
        }, name='feeds'),
)

if 'pingback' in settings.INSTALLED_APPS:
    from django_xmlrpc.views import handle_xmlrpc
    urlpatterns += patterns('',
        url(r'^xmlrpc/$', handle_xmlrpc, name='xmlrpc'),
    )

urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/$', blog_views.post_detail, name='blog_detail'),
)
