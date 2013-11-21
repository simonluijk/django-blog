import re

from django import template
from django.db import models

Post = models.get_model('blog', 'post')
Category = models.get_model('blog', 'category')

register = template.Library()


class LatestPosts(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name

    def render(self, context):
        posts = Post.objects.published()[:int(self.limit)]
        if posts and (int(self.limit) == 1):
            context[self.var_name] = posts[0]
        else:
            context[self.var_name] = posts
        return ''


@register.tag
def get_latest_posts(parser, token):
    """
    Get any number of latest posts and stores them in a varable.

    Syntax::
        {% get_latest_posts [limit] as [var_name] %}

    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        msg = "%s tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        msg = "%s tag had invalid arguments" % tag_name
        raise template.TemplateSyntaxError(msg)
    format_string, var_name = m.groups()
    return LatestPosts(format_string, var_name)


class BlogCategories(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        categories = Category.objects.all()
        context[self.var_name] = categories
        return ''


@register.tag
def get_blog_categories(parser, token):
    """
    Gets all blog categories.

    Syntax::
        {% get_blog_categories as [var_name] %}

    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        msg = "%s tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    m = re.search(r'as (\w+)', arg)
    if not m:
        msg = "%s tag had invalid arguments" % tag_name
        raise template.TemplateSyntaxError(msg)
    var_name = m.groups()[0]
    return BlogCategories(var_name)
