from django.conf.urls.defaults import *
from ddtcms.faq.models import Faq
faq_dict = {
'queryset': Faq.objects.all(),
}


urlpatterns = patterns('django.views.generic',
    (r'^$',                   'date_based.archive_index', dict(faq_dict,date_field='pub_date')),
    (r'^(?P<slug>[-\w]+)/$',  'list_detail.object_detail',dict(faq_dict,slug_field='slug')),
)
