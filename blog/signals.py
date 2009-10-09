import markdown

from django.conf import settings
from django.db.models.signals import post_save
from django.utils.encoding import smart_str, force_unicode
from django.core.urlresolvers import reverse

from blog.models import Post


def get_html(instance):
    # markdown.version was first added in 1.6b. The only version of markdown
 	# to fully support extensions before 1.6b was the shortlived 1.6a.

    # Unicode support only in markdown v1.7 or above. Version_info
    # exist only in markdown v1.6.2rc-2 or above.
 	if not hasattr(markdown, 'version') or getattr(markdown, 'version_info', None) < (1,7):
 	    return force_unicode(markdown.markdown(smart_str(instance.body)))
 	else:
 	    return markdown.markdown(force_unicode(instance.body))


def get_feed_url(instance):
    return reverse('feeds', args=['latest'])


def create_signal(signal_creator):
    try:
        signal = signal_creator(content_func=get_html, feed_url_fun=get_feed_url)
    except TypeError:
        signal = signal_creator(content_func=get_html)

    def inner_func(instance, **kwargs):
        if instance.status == 2:
            signal(instance, **kwargs)
    return inner_func


if 'pingback' in settings.INSTALLED_APPS:
    from pingback.client import ping_external_links, ping_directories
    post_save.connect(create_signal(ping_external_links), sender=Post, weak=False)
    post_save.connect(create_signal(ping_directories), sender=Post, weak=False)
