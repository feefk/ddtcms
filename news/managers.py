# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: managers.py
# Creation Date: 2011-11-05  23:57
# Last Modified: 2011-11-12 17:19:12
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


class NewsManager(models.Manager):
	def get_approved(self):
		return self.filter(approved = True)
	def get_published(self):
		#return self.filter(status__gt=0, pub_date__lte=datetime.datetime.now)
		return self.filter(approved = True)
	def get_privated(self):
		return self.filter(status__exact=0)
	def get_headlines(self):
		return self.filter(status__exact=1)
	def get_recommended(self):
		return self.filter(status__exact=2)
	def get_flashslide(self):
		return self.filter(gallery__isnull = False)
	def for_user(self,user):
		return self.filter(deliverer=user)
		
	def for_category(self,category):
		return self.filter(category=category)
	def for_categories(self,category):
		categories=category.get_all_children()
		categories.append(category)
		return self.filter(category__in=categories)
