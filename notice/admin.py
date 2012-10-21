# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: admin.py
# Creation Date: 2009-06-15  21:23
# Last Modified: 2011-11-12 17:23:2
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
from ddtcms.notice.models import Notice
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------



class NoticeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug','type','pub_date','over_date')
    list_filter = ['type']
    search_fields = ['title','slug']
    

admin.site.register(Notice,NoticeAdmin)

