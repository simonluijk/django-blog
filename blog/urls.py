from django.conf.urls import patterns, url

from .views import PostListView, PostDetailView
from .feeds import LatestFeed, CategoryFeed


urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name='index'),

                       url(r'^topic/(?P<slugs>[-\w/]+)/$',
                           PostListView.as_view(), name='category'),

                       url(r'^feed/$', LatestFeed(), name='feed_latest'),

                       url(r'^feed/(?P<slugs>[-\w/]+)/$', CategoryFeed(),
                           name='feed_category'),

                       url(r'^(?P<slug>[-\w]+)/$', PostDetailView.as_view(),
                           name='detail'))
