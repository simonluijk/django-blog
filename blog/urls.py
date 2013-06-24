from django.conf.urls import patterns, url

from .views import PostDetailView, PostListView, CategoryPostListView


urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='blog_index'),
    url(r'^topic/(?P<slugs>[-\w/]+)/$', CategoryPostListView.as_view(),
        name='blog_category'),
    url(r'^(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='blog_detail'),
)
