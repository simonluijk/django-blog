from django.conf import settings
from blog.models import Post

if 'pingback' in settings.INSTALLED_APPS:
    from pingback import register_pingback, ping_func
    from django_xmlrpc import xmlrpcdispatcher

    def pingback_handler(slug, **kwargs):
        return Post.objects.get(slug=slug)

    register_pingback('blog.views.post_detail', pingback_handler)
    xmlrpcdispatcher.register_function(ping_func, 'pingback.ping')
