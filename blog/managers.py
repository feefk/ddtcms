# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: managers.py
# Creation Date: 2009-06-08  20:56
# Last Modified: 2011-11-12 16:59:30
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#
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

class BlogManager(models.Manager):
    def for_user(self, user):
        user_blogs = Q(user__exact=user)
        return self.filter(user_blogs)
