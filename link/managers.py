# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: managers.py
# Creation Date: 2011-11-04  21:58
# Last Modified: 2011-11-12 17:14:0
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import datetime
#import urllib
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





class CategoryManager(models.Manager):
    def get_all_roots(self):
        return self.filter(parent__isnull = True)


class LinkManager(models.Manager):
    
    def for_category(self,category):
        return self.filter(category=category)
        
    def for_user(self,user):
        return self.filter(author=user)

    def for_categories(self,category):
        categories=category.get_all_children()
        categories.append(category)
        return self.filter(category__in=categories)
