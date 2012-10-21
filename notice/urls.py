# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: urls.py
# Creation Date: 2011-04-23  22:25
# Last Modified: 2011-11-12 18:31:15
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
from ddtcms.notice.models import Notice
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
info_dict = {
'queryset': Notice.objects.all(),
}
# ------------------------------------------------------------

urlpatterns = patterns('django.views.generic',
    url(r'^$',                'date_based.archive_index', dict(info_dict,date_field='pub_date'), name="notice_index"),
    url(r'^(?P<slug>[-\w]+)/$',  'list_detail.object_detail',dict(info_dict,slug_field='slug'),  name="notice_detail"),
)
