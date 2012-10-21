# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: urls.py
# Creation Date: 2011-11-04  18:34
# Last Modified: 2011-11-12 17:11:55
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.conf.urls.defaults import *
from django.conf import settings
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



urlpatterns = patterns('',
    (r'^$',                    'ddtcms.home.views.index'),
    #(r'^favicon.ico$',        'ddtcms.home.views.favicon'),  
    (r'^(?i)favicon.ico$',     'django.views.static.serve', {'path':'favicon.ico','document_root' : settings.STATIC_ROOT})
)
