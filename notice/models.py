# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: models.py
# Creation Date: 2009-06-13  01:15
# Last Modified: 2011-11-12 18:28:50
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.news.models import News
from ddtcms.news.signals import latest_news_created
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
NOTICE_TYPE= (
    (0,  _('SITE NOTICE')),
    (1,  _('USER ACTION')),
    (2,  _('APP NOTICE')),
    (3,  _('OTHER TYPE')),
)
# ------------------------------------------------------------

# Create your models here.
class Notice(models.Model):
    title         = models.CharField(max_length=200)
    slug          = models.SlugField(max_length=50)
    content       = models.TextField()
    pub_date      = models.DateTimeField('date published', default=datetime.datetime.now())
    over_date     = models.DateTimeField('date overed', default=datetime.datetime.now()+datetime.timedelta(days=30))
    type          = models.PositiveSmallIntegerField(blank=True,choices=NOTICE_TYPE,default=0)
    
    
    class Meta:
        ordering            =  ('-pub_date',)
        verbose_name        = _('Notice')
        verbose_name_plural = _('Notices')
        
    def __unicode__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.slug = self.slug.lower().replace('-','_')
        super(Notice,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return "/notice/%s/" % (self.slug)

#def my_handler(sender, **kwargs):
#	created        = kwargs['created']
#	the_added_news = kwargs['instance']
#	if created:
#		new_notice=Notice()
#		new_notice.title= _("%s Posted A new News:%s") % ( the_added_news.deliverer, the_added_news.title)
#		new_notice.content=the_added_news.summary + the_added_news.deliverer.name # if not .name error ocured,unicode error
#		new_notice.slug='news%s' % the_added_news.id
#		new_notice.save()
#
#signals.post_save.connect(my_handler, sender=News)


def latest_entry_created_handler(sender, **kwargs):
	new_notice=Notice()
	new_notice.title   = kwargs['title']
	new_notice.content = kwargs['content']
	new_notice.slug    = kwargs['slug']
	new_notice.save()


latest_news_created.connect(latest_entry_created_handler, sender=News)

