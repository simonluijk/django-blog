from django.conf.urls.defaults import *
from blog import views as blog_views
from blog.feeds import BlogPostsFeed, BlogPostsByCategoryFeed

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$',
        view=blog_views.post_detail,
        name='blog_detail'),

    url(r'^archive/(?P<year>\d{4})/(?P<month>\w{3})/$',
        view=blog_views.post_archive_month,
        name='blog_archive_month'),

    url(r'^archive/(?P<year>\d{4})/$',
        view=blog_views.post_archive_year,
        name='blog_archive_year'),

    url(r'^topic/(?P<slugs>[-\w/]+)/$',
        view=blog_views.category,
        name='blog_category'),

    url(r'^$',
        view=blog_views.post_list,
        name='blog_index'),

    url(r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', {
            'feed_dict': {
                'latest': BlogPostsFeed,
                'topic': BlogPostsByCategoryFeed,
            }
        },
        name='feeds'),
)
