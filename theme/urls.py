# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: urls.py
# Creation Date: 2011-04-23  22:24
# Last Modified: 2011-11-12 18:37:15
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
from ddtcms.theme.models import Theme
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
todo_dict = {
'queryset': Project.objects.all().filter(type__exact=0),
}
todo_dict.update({'date_field': 'pub_date',})

pages_dict = {
'queryset': Project.objects.all(),
'paginate_by':1,
}
# ------------------------------------------------------------




urlpatterns = patterns('',
    #url(r'^$','todo.views.index',name='todo'),
    #(r'^$',                   'django.views.generic.date_based.archive_index', todo_dict),
    url(r'^$',             'todo.views.index',name='todo-index'),
    url(r'^manage/$',             'todo.views.manage',name='todo-manage'),
    (r'^(?P<object_id>\d+)/$',      'django.views.generic.list_detail.object_detail', dict(queryset=Project.objects.all())),
    (r'^(?P<slug>[-\w]+)/$',   'django.views.generic.list_detail.object_detail', dict(queryset=Project.objects.all(),slug_field='slug')),
    (r'^task/add/',            'todo.views.task_add'),
    (r'^task/done/',           'todo.views.task_done'),
    (r'^task/undone/',         'todo.views.task_undone'),
    (r'^task/delete/',         'todo.views.task_del'),
    (r'^project/add/',         'todo.views.project_add'),
    (r'^project/delete/',      'todo.views.project_del'),
    (r'^project/change_type/', 'todo.views.project_chg_type'),
    
)