from django.conf.urls.defaults import patterns, url
from blog import views as blog_views


urlpatterns = patterns('',
    url(r'^$', blog_views.post_list, name='blog_index'),
    url(r'^topic/(?P<slugs>[-\w/]+)/$', blog_views.category, name='blog_category'),
    url(r'^(?P<slug>[-\w]+)/$', blog_views.post_detail, name='blog_detail'),
)
