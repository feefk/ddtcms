# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: feeds.py
# Creation Date: 2008-12-26  00:29
# Last Modified: 2011-11-12 17:17:45
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from news.models import NewsItem
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------




class NewsFeed(Feed):

	def title(self):
		return u"%s" % Site.objects.get_current().name

	def description(self):
		return u'Latest news from %s' % Site.objects.get_current().name

	def link(self):
		# return reverse('news-index')
		return '/news/'

	def items(self):
		return NewsItem.on_site.published(5)
		
	def item_pubdate(self, item):
		from datetime import datetime
		return datetime(item.date.year, item.date.month, item.date.day)