# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: admin.py
# Creation Date: 2011-02-25  23:29
# Last Modified: 2011-11-12 18:35:12
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.contrib import admin

# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.theme.models import Theme,Template
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------




class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name','desc','as_default')
  
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name','last_changed','theme_ids')
  

admin.site.register(Theme,ThemeAdmin)
admin.site.register(Template,TemplateAdmin)