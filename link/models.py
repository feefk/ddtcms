# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: models.py
# Creation Date: 2011-11-05  00:37
# Last Modified: 2011-11-12 17:14:41
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import os
import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db import models

from django.contrib.auth.models import User
from django.utils.encoding import force_unicode,smart_unicode, smart_str, DEFAULT_LOCALE_ENCODING
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
from link.managers import LinkManager
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
    user          = models.ForeignKey(User, blank=True, null=True, related_name="link_categories")
    name          = models.CharField(_('name'), max_length=50)
    slug          = models.SlugField(max_length=50,help_text='alias to the name,use english')
    parent        = models.ForeignKey('self',null=True,blank=True,related_name='link_category_child')
    is_public     = models.BooleanField(_('is public'), default=True,
                                help_text=_('Public links will be displayed.'))
    depth         = models.PositiveSmallIntegerField(_("category's depth"), blank=True,null=True)
    display_order = models.PositiveSmallIntegerField(_('order'), default=1)


    class Meta:
        verbose_name = _('Link Category')
        verbose_name_plural = _('Link Categories')



    def __unicode__(self):
        return self.name

    def get_children(self):
        return self.link_category_child.all()

    def is_root(self):
        if self.parent == None:
            return True
        return False

    def get_absolute_url(self):
        return "/link/category/%s/" %  self.slug

class Link(models.Model):
    title     = models.CharField(max_length=200)
    category  = models.ForeignKey(Category,blank=True,null=True,related_name='child_links')
    url       = models.URLField(max_length=255,default='http://',verify_exists=False)
    domain    = models.CharField(null=True,blank=True,max_length=255,help_text='like "sohu.com" in "www.sohu.com",or IP:"127.0.0.1"')
    slug      = models.SlugField(null=True,blank=True,help_text='Automatically built From the domain.')
    notes     = models.TextField(null=True,blank=True)
    pub_date  = models.DateTimeField(null=True,blank=True,default=datetime.datetime.now)
    tags      = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))

    objects = LinkManager()
    
    class Meta:
        ordering            =  ('-pub_date','title','slug',)
        verbose_name        = _('Link')
        verbose_name_plural = _('Links')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


class CGPUpload(models.Model):
    cgp_file    = models.FileField(_('group file (.cgp)'), upload_to="upload/temp",
                                help_text=_('Select a .cgp file of links to upload into a new Category.'))
    category    = models.ForeignKey(Category, null=True, blank=True, help_text=_('Select a category to add these links to.'))

    class Meta:
        verbose_name = _('group file (.cgp) upload')
        verbose_name_plural = _('group file (.cgp) uploads')

    def save(self, *args, **kwargs):
        super(CGPUpload, self).save(*args, **kwargs)
        category = self.process_cgpfile()
        super(CGPUpload, self).delete()
        return category

    def process_cgpfile(self):
        if os.path.isfile(self.cgp_file.path):
            # TODO: implement try-except here
            lines=[]

            try:
                fp=file(self.cgp_file.path) # if no mode is specified, 'r'ead mode is assumed by default
            except:
                raise Exception('Error occured when open then file "%s".' % self.cgp_file.path)

            while True:
                line = fp.readline()
                if len(line) == 0: # Zero length indicates EOF
                    break
                line=line.rstrip()
                try:
                    line = smart_unicode(line,DEFAULT_LOCALE_ENCODING)
                except UnicodeDecodeError:
                    line = "" # ignore this line
                lines.append(line)
                #    print line,
            # Notice comma to avoid automatic newline added by Python
            fp.close() # close the file


            d={}
            for it in lines:
                if it[0:3]=="dow" or it[0:3]=="[Gr" or len(it) < 3:
                    #lines.remove(it)
                    continue
                else:
                    #print it.split('=')
                    key,value = it.split('=',1)
                    if value == '': # drop the empty url
                        continue
                    d[key] = value

            if self.category:
                category = self.category
            else:
                raise Exception('must choose a category')
                #category = Category.objects.create(
                #user 
                #name = os.path.splitext(os.path.basename(self.cgp_file.path))[0]
                #)

            for key in d.keys():
                if key[0:4]=='name':
                    #i=int(key[4:])
                    #print d[key],'=',d['url'+key[4:]]
                    title = d[key]
                    try:
                        url   = d['url'+key[4:]]
                    except KeyError:
                        continue
                    
                    link=Link(
                        title    = title,
                        category = category,
                        url      = url,
                        notes    = title,
                        pub_date = datetime.date.today(),
                    )
                    link.save()

            return category