from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from blog.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('title', 'parent')
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status')
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 'body', 'tease', 'categories', 'status'
            ),
        }),
        (_('Extra info'), {
            'classes': ('collapse',),
            'fields': (
                'allow_comments', 'slug', 'publish'
            ), 
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
