# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: urls.py
# Creation Date: 2011-04-23  22:29
# Last Modified: 2011-11-12 17:6:29
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import DetailView, ListView

from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, \
                                        WeekArchiveView, DayArchiveView, TodayArchiveView, \
                                        DateDetailView
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.blog.models import Blog
from ddtcms.blog.models import Category
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
extra_context = {
    'latest_Blog_list':Blog.objects.all()[:5],
    'category_list'  : Category.objects.all(),
}
    
blog_dict = {
'queryset': Blog.objects.all(),
'extra_context':extra_context,
}


category_dict = {
'queryset': Category.objects.all(),
'extra_context':extra_context,
}

pages_dict = {
'queryset': Blog.objects.all(),
'paginate_by':3,
}

archive_dict={}
archive_dict.update(blog_dict)
archive_dict.update({'date_field': 'pub_date',})
    
# ------------------------------------------------------------
#
# paginator = Paginator(Blog.objects.all().order_by('-pub_date'), 3)
#  latest_post_list = paginator.page(1).object_list
#  catalog_list = Category.objects.all()  
#  page_list = [i for i in paginator.page_range ]
#  return render_to_response('blog_index.html',{
#    'latest_post_list': latest_post_list,
#    'catalog_list': catalog_list,
#    'blog_roll': blog_roll,
#    'page_list': page_list,
#    })


urlpatterns = patterns('',

    
    url(r'^page/(?P<page>\w+)/$',          
        ListView.as_view(
            queryset            = Blog.objects.all(),
            context_object_name = 'latest_blog_list',
            paginate_by         = 3
        ),
        name='blog_pages'),


    
    #url(r'^(?P<pk>\d+)/$',
    #    DetailView.as_view(
    #        model=Blog,
    #    name='blog_detail'),
    
    url(r'^category/$',          
        ListView.as_view(
            queryset            = Category.objects.all(),
            context_object_name = 'latest_blog_list',
            paginate_by         = 3
        ),
        name='category_list'),
    
    url(r'^category/(?P<slug>[-\w]+)/$',          
        DetailView.as_view(
            model               = Category,
            context_object_name = 'category',
        ),
        name='category_detail'),
        
    url(r'^archive/$',                     
        ArchiveIndexView.as_view(
            queryset            = Blog.objects.all(),
            date_field          = 'pub_date',
        ),
        name='blog_archive_index'),
        
    url(r'^archive/(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset            = Blog.objects.all(),
            date_field          = 'pub_date',
        ),
        name='blog_archive_index_year'),
    
    
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            queryset            = Blog.objects.all(),
            date_field          = 'pub_date',
            month_format        = '%m'
        ),
        name='blog_archive_index_month'),
    
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/$',
        MonthArchiveView.as_view(
            queryset            = Blog.objects.all(),
            date_field          = 'pub_date',
            month_format        = '%m'
        ),
        name='blog_archive_index_day'),
    
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',          
        DateDetailView.as_view(
            model               = Blog,
            context_object_name = 'blog',
            date_field          = 'pub_date',
            month_format        = '%m'
        ),
        name='blog_detail'),
    
    url(r'^$',     'ddtcms.blog.views.index',name='blog_index'),
    url(r'^post/$','ddtcms.blog.views.post'),
    
)

