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
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from theme.models import Theme
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------


def load_template_source(template_name, template_dirs=None):
    """
    Tries to load the template from the dbtemplates cache backend specified
    by the DBTEMPLATES_CACHE_BACKEND setting. If it does not find a template
    it falls back to query the database field ``name`` with the template path
    and ``sites`` with the current site.
    """
    cachename = 'current_theme'
    timeout = 60*60*24

    theme = cache.get(cachename)
    if theme is None:
    	theme= Theme.objects.get_current() #or Settings.get_current_theme()
        cache.set(cachename, theme, timeout)
    
    theme_dir = "default"
    if theme:
        theme_dir= theme.path
    
    template_dirs = [ os.path.join(settings.THEME_ROOT, theme_dir, 'templates'),]
    return django_load_template_source(template_name, template_dirs)
load_template_source.is_usable = True
