# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: models.py
# Creation Date: 2010-03-09  11:12
# Last Modified: 2011-11-12 17:4:39
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------

# 3dpart.
# attempt to load the django-tagging TagField from default location,
# otherwise we substitude a dummy TagField.
try:
    from tagging.fields import TagField
    tagfield_help_text = _('Separate tags with spaces, put quotes around multiple-word tags.')
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = _('Django-tagging was not found, tags will be treated as plain text.')
# ------------------------------------------------------------

# ddtcms.
from blog.managers import BlogManager
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------


# Create your models here.
class Category(models.Model):
    user          = models.ForeignKey(User, blank=True, null=True, related_name="blog_categories")
    name          = models.CharField(_('name'), max_length=50)
    slug          = models.SlugField(max_length=50,help_text='alias to the name,use english')
    parent        = models.ForeignKey('self',null=True,blank=True,related_name='category_child')
    depth         = models.PositiveSmallIntegerField(_("category's depth"), blank=True,null=True)
    display_order = models.PositiveSmallIntegerField(_('order'), default=1)


    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=( self.slug,))

    def get_children(self):
        return self.category_child.all()

    def is_root(self):
        if self.parent == None:
            return True
        return False



class Blog(models.Model):
    title         = models.CharField(max_length=200)
    pub_date      = models.DateTimeField('date published',blank=True,default=datetime.datetime.now)
    content       = models.TextField()
    user          = models.ForeignKey(User,verbose_name='Author', editable=False)
    category      = models.ForeignKey(Category,null=True)
    slug          = models.SlugField(
                      unique_for_date='pub_date',
                      help_text='Automatically built From the title.'
                  )
    summary       = models.TextField(help_text="One paragraph. Don't add tag.")
    tags          = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))
    views         = models.PositiveIntegerField(_("Views"), default=0)
    comments      = models.PositiveIntegerField(_("Comments"), default=0)

    objects       = BlogManager()

    class Meta:
        ordering            = ('-pub_date',)
        verbose_name        = _('Blog')
        verbose_name_plural = _('Blogs')
#        get_latest_by = 'pub_date'
#        db_table      = "blog_entry"



    def get_absolute_url(self):
        return reverse('blog_detail', args=(self.pub_date.year, self.pub_date.month,self.pub_date.day, self.slug))

    def __unicode__(self):
        return self.title
        
