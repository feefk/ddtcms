# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: urls.py
# Creation Date: 2011-11-04  23:48
# Last Modified: 2011-11-12 17:15:36
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.conf.urls.defaults import *
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.link.models import Link
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
info_dict = {
    'queryset': Link.objects.all(),
}

# ------------------------------------------------------------








urlpatterns = patterns('',
    (r'^$',                               'django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$',            'django.views.generic.list_detail.object_detail', info_dict),
    #(r'^(?P<object_id>\d+)/$',            'django.views.generic.list_detail.object_detail', info_dict),
)

urlpatterns = patterns('ddtcms.link.views',
	url(r'^$',                          'index',       name="link_index"),
	url(r'^add/$',                      'link_create', name="link_create"),
	url(r'^(?P<object_id>\d+)/$',       'link_detail', name="link_detail"),
	url(r'^(?P<object_id>\d+)/edit/$',  'link_change', name="link_change"),
	url(r'^(?P<object_id>\d+)/del/$',   'link_delete', name="link_delete"),
	url(r'^import/$',                   'link_import', name='link_import'),
    url(r'^export/$',                   'link_export', name='link_export'),
    
    url(r'^categor(y|ies)/$','category_list',name='link-categories'),
    url(r'^category/(?P<category_slug>.+)/$','by_category',name='links-by-category'),
)
