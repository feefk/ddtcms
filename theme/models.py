# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: models.py
# Creation Date: 2011-11-04  15:55
# Last Modified: 2011-11-12 18:36:31
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
from datetime import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db import models
from django.conf import settings
from django.db.models import signals
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext as _
from django.template import TemplateDoesNotExist
from django.template.loader import find_template_source
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from theme.managers import ThemeManager
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------

class Theme(models.Model):
    name        = models.CharField(_('Theme Name'),max_length=255)
    path        = models.CharField(_('The path where theme stored'),max_length=255)
    desc        = models.CharField(_('Theme Description'),max_length=1024,null=True,blank=True)
    css         = models.TextField(_('Theme default css text'),blank=True)
    #sites       = models.ManyToManyField(Site,verbose_name=_('Sites belongs to'),related_name='site_themes', default=[settings.SITE_ID])
    sites       = models.ManyToManyField(Site,verbose_name=_('Sites belongs to'), default=[settings.SITE_ID])
    as_default  = models.BooleanField(_("As Default Theme"), default=False)
    
    objects = ThemeManager()  #models.Manager()
    #on_site = CurrentSiteManager('sites')
    
    def __unicode__(self):
        return self.name    
        
    def get_absolute_url(self):
        return "/themes/%s/" % (self.id)
            
    class Meta:
        ordering            = ('id',)
        verbose_name        = _('Theme')
        verbose_name_plural = _('Themes')
    
    def save(self,*args,**kwargs):
        cachename = 'current_theme'
        cache.delete(cachename)
        if not self.desc:
            self.desc = self.name
        super(Theme,self).save(*args,**kwargs)

def get_current_theme():
    cachename = 'current_theme'
    timeout = 60*60*24

    theme = cache.get(cachename)
    if theme is None:
        theme= Theme.objects.get_current()
        cache.set(cachename, theme, timeout)

    return theme        
        
class Template(models.Model):
    """
    Defines a template model for use with the database template loader.
    The field ``name`` is the equivalent to the filename of a static template.
    """
    name          = models.CharField(_('name'), unique=True, max_length=100, help_text=_("Example: 'flatpages/default.html', or 'index.html'"))
    content       = models.TextField(_('content'), blank=True)
    themes        = models.ManyToManyField(Theme)
    theme_ids     = models.CharField(_('theme ids'), max_length=100, help_text=_("Auto Generated like: '0,1,2'"),default='0')
    creation_date = models.DateTimeField(_('creation date'), default=datetime.now)
    last_changed  = models.DateTimeField(_('last changed'), default=datetime.now)

    objects = models.Manager()

    class Meta:
        unique_together     = (("theme_ids", "name"),)
        verbose_name        = _('template')
        verbose_name_plural = _('templates')
        ordering            = ('name',)

    def __unicode__(self):
        return self.name
    

    def get_theme_ids(self):
        ids =''
        tl=[]
        if self.themes:
            for theme in self.themes.all():
                tl.append(theme.id)
            ids = ','.join(map(str, tl))
        else:
            ids = '0'
        return ids

    def save(self,*args,**kwargs):
        super(Template,self).save(*args,**kwargs)#save first to genarate themes ManyToMany relation
        self.theme_ids = self.get_theme_ids()
        super(Template,self).save(*args,**kwargs)

