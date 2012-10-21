# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: signals.py
# Creation Date: 2009-05-21  11:07
# Last Modified: 2011-11-12 18:30:48
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db.models import signals
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.notice.models import Notice
from ddtcms.news.models import News
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------



def my_handler(sender, **kwargs):
    new_notice=Notice()
    new_notice.title="A new News Posted"
    new_notice.content='content'
    new_notice.slug='news%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_notice.save()
signals.post_save.connect(my_handler, sender=News)
