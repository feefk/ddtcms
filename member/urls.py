from django.conf.urls.defaults import *
from ddtcms.member.models import Profile,Resume

    
    
member_dict = {
'queryset': Profile.objects.all(),
'template_name':'member/index.html',
}


pages_dict = {
'queryset': Profile.objects.all(),
'paginate_by':1,
}


urlpatterns = patterns('',
    (r'^$',                            'django.views.generic.list_detail.object_list', member_dict),
)
