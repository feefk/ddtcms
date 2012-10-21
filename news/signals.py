# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: signals.py
# Creation Date: 2009-05-21  13:04
# Last Modified: 2011-11-12 17:20:29
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.contrib.comments.signals import comment_will_be_posted
from django.contrib.comments.models import Comment
from django.http import HttpResponseRedirect

from django.dispatch import Signal

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


latest_news_created = Signal(providing_args=["title","content","slug"])

#def unapprove_comment(sender, **kwargs):
#	the_comment = kwargs['comment']
#	the_comment.is_public = False
#	return True
#	
#comment_will_be_posted.connect(unapprove_comment)




    

