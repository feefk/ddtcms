# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: sitemaps.py
# Creation Date: 2009-02-05  23:25
# Last Modified: 2011-11-12 17:5:58
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.contrib.sitemaps import Sitemap
from ddtcms.blog.models import Blog
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



class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.pub_date
