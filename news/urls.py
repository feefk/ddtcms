# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Script   Name: urls.py
# Creation Date: 2011-03-17  23:09
# Last Modified: 2011-11-12 17:21:6
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, \
                                        WeekArchiveView, DayArchiveView, TodayArchiveView, \
                                        DateDetailView
# ------------------------------------------------------------

# 3dpart.
from tagging.models import Tag
# ------------------------------------------------------------

# ddtcms.
from ddtcms.news.models import News,Category
from ddtcms.news.views  import NewsDetailView,CategoryNewsListView
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
try:
    PAGINATE = settings.NEWS_PAGINATE_BY
except:
    PAGINATE = 8

news_dict = {
'queryset': News.objects.all(),
'extra_context':{'categories':Category.objects.all()}
}

# ------------------------------------------------------------



urlpatterns = patterns('',
    url(r'^page/(?P<page>\w+)/$',
        ListView.as_view(
            queryset            = News.objects.all(),
            context_object_name = 'latest_blog_list',
            paginate_by         = 3
        ),
        name='news_pages'),



    #url(r'^(?P<pk>\d+)/$',
    #    DetailView.as_view(
    #        model=Blog,
    #    name='news_detail'),

    url(r'^category/$',
        ListView.as_view(
            queryset            = Category.objects.all(),
            context_object_name = 'latest_blog_list',
            paginate_by         = 3
        ),
        name='news_category_list'),

    url(r'^category/(?P<slug>[-\w]+)/$',
        CategoryNewsListView.as_view(),
        name='news_category_detail'),

    #url(r'^$',
    #    ArchiveIndexView.as_view(
    #        queryset            = News.objects.all(),
    #        date_field          = 'pub_date',
    #    ),
    #    name='news_archive_index'),

    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset            = News.objects.all(),
            date_field          = 'pub_date',
            make_object_list    = True
        ),
        name='news_archive_index_year'),


    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            queryset            = News.objects.all(),
            date_field          = 'pub_date',
            month_format        = '%m'
        ),
        name='news_archive_index_month'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/$',
        MonthArchiveView.as_view(
            queryset            = News.objects.all(),
            date_field          = 'pub_date',
            month_format        = '%m'
        ),
        name='news_archive_index_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        NewsDetailView.as_view(
            date_field          = 'pub_date',
            month_format        = '%m'
        ),
        name='news_detail'),



    url(r'^year/(?P<year>\d{4})/$','by_year',name='news_by_year'),#url(r'^$', 'object_list', dict(news_dict, paginate_by=PAGINATE,template_name='news/news_index.html'), name="news-index"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'view', name="news-item"),
    #url(r'^(?P<object_id>\d+)/$',
    #    DetailView(
    #        model               = News,
    #        context_object_name = 'news_item',
    #    ),
    #    name="news-item-id"),

    url(r'^tag/(?P<tag>.+)/$','by_tag',name='news-by-tag'),
    #url(r'^tags/$',
    #    ListView.as_view(
    #        queryset            = Tag.objects.all(),
    #        context_object_name = 'tag_list',
    #        paginate_by         = 30
    #    ),
    #    name='news_tag_list'),

    #url(r'^tags/(?P<slug>[-\w]+)/$',
    #    DetailView(
    #        model               = Tag,
    #        context_object_name = 'tag',
    #    ),
    #    name="news_tag"),

)

urlpatterns += patterns('ddtcms.news.views',
    url(r'^$',     'index',name='news_index'),
    #url(r'^authors/$','author_list',name='news-authors'),
    #url(r'^authors/(?P<author_slug>.+)/$','by_author',name='news-by-author'),
    url(r'^categor(y|ies)/$','category_list',name='news-categories'),
#    #url(r'^category/(?P<category_slug>.+)/$','by_category',name='news-by-category'),

    url(r'^post/$','post', name='news-post'),
    url(r'^search/$','search',name='news_search_index'),
    url(r'^search/(?P<keywords>.+)/$','search',name='news_search_keywords'),
    
    url(r'^(?P<slug>[-\w]+)/$',
            CategoryNewsListView.as_view(),
            name='news_list_by_category'),

    
    url(r'^([-\w/]+/)(?P<slug>[-\w]+)/$', 
        CategoryNewsListView.as_view(), 
        name='news_list_by_subcategory'),
    
    url(r'^(?P<category>[-\w]+)/post/$', 'post', name='news-newitem'),
    url(r'^([-\w/]+/)(?P<category>[-\w]+)/post/$', 'post'),

    #url(r'^category/(?P<category_slug>.+)/$','by_category',name='news-by-category'),
    #url(r'^categor(y|ies)/$','category_list',name='news-categories'),

)
