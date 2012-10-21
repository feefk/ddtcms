from django.conf.urls.defaults import *
from tagging.views import tagged_object_list

urlpatterns = patterns('',
    #(r'^$',                    'django.views.generic.date_based.archive_index', todo_dict),
    url(r'^$',                  'tagging.views.index', name='tagging-index'),
    url(r'^(?P<tag>[-\w]+)/$',  'tagging.views.by_tag',name='tagged_object_list'),
)

urlpatterns += patterns('',
    url(r'^tr/(\d+)/(\w+)/$', 'django.views.defaults.shortcut', name='tag-url-redirect'),
)