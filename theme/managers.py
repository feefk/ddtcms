# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: managers.py
# Creation Date: 2011-02-25  23:33
# Last Modified: 2011-11-12 18:36:16
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db import models
from django.db.models import Q
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
#from models import MODEL
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------



class ThemeManager(models.Manager):
    def for_site(self, site):
        site_themes = Q(sites__exact=site)
        return self.filter(site_themes)
        
    def get_current(self):
        current_theme = None
        query = Q(as_default__exact=True)
        try:
            themes = self.filter(query)
            if themes:
                current_theme = themes[0]
        except KeyError,IndexError:
            pass
        return current_theme
    
    def clear_default_state(self):
        pass
