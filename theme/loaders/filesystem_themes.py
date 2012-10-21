# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: loader.py
# Creation Date: 2011-03-25  00:24
# Last Modified: 2011-11-12 18:35:34
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import os
#import urllib
# ------------------------------------------------------------

# django.
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.template.loaders.filesystem import load_template_source as django_load_template_source
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache
from django.template import  Template

# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from theme.models import Theme
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#
# ------------------------------------------------------------
from django.template.loaders import filesystem

class Loader(filesystem.Loader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        
        cachename = 'current_theme'
        timeout = 60*60*24 # one day
    
        theme = cache.get(cachename,None)
        if theme is None:
            theme= Theme.objects.get_current() #or Settings.get_current_theme()
            cache.set(cachename, theme, timeout)
        
        theme_dir = "default"
        if theme:
            theme_dir= theme.path
        
        #overwrite template_dirs, whatever template_dirs is None or not
        template_dirs = [ os.path.join(settings.THEME_ROOT, theme_dir, 'templates'),]
        
        source, origin = self.load_template_source(template_name, template_dirs)
        template = Template(source)
        return template, origin


_loader = Loader()

def load_template_source(template_name, template_dirs=None):
    # For backwards compatibility
    import warnings
    warnings.warn(
        "'django.template.loaders.filesystem.load_template_source' is deprecated; use 'django.template.loaders.filesystem.Loader' instead.",
        DeprecationWarning
    )
    return _loader.load_template_source(template_name, template_dirs)
load_template_source.is_usable = True
