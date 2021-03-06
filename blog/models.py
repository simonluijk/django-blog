import mptt

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.db.models import permalink
from blog.managers import PostManager, CategoryManager


class Category(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), null=True,
                               blank=True, related_name='children')
    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return u'%s' % self.title

    def get_slugs(self):
        slugs = []
        for category in self.get_ancestors():
            slugs.append(category.slug)
        slugs.append(self.slug)
        return slugs

    @permalink
    def get_absolute_url(self):
        slugs = u'/'.join(self.get_slugs())
        return ('blog:category', None, {
            'slugs': slugs
        })

    @permalink
    def get_feed_absolute_url(self):
        slugs = u'/'.join(self.get_slugs())
        return ('blog:feed_category', None, {
            'slugs': slugs
        })


mptt.register(Category, order_insertion_by=['title', ])


class Post(models.Model):
    DRAFT = 1
    PUBLISHED = 2
    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    body = models.TextField(_('body'))
    tease = models.TextField(_('tease'), blank=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES,
                                 default=1)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=now)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))
    created = models.DateTimeField(_('created'), editable=False)
    modified = models.DateTimeField(_('modified'), editable=False)
    objects = PostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-publish', )
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog:detail', None, {'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = now()
        self.modified = now()
        super(Post, self).save(*args, **kwargs)

    def get_previous_post(self):
        """
        Return previous post
        """
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        """
        Return next post
        """
        return self.get_next_by_publish(status__gte=2)
