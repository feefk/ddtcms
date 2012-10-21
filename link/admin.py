# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: admin.py
# Creation Date: 2010-04-24  13:18
# Last Modified: 2011-11-12 17:13:0
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
from ddtcms.link.models import Link
from ddtcms.link.models import Category
from ddtcms.link.models import CGPUpload
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url','category', 'slug',  'pub_date')
    list_filter = ('category', 'domain')
    ordering = ('url',)
    search_fields = ('title', 'url')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user','slug','display_order')
    list_filter = ('user',)
class CGPUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button
        
        
admin.site.register(Link, LinkAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(CGPUpload,CGPUploadAdmin)



