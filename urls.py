from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from ddtcms.blog.sitemaps import BlogSitemap
from ddtcms.blog.models import Blog

from ddtcms.member.views import get_profiles


from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

admin.site.add_action(export_selected_objects)

info_dict = {
    'queryset': Blog.objects.all(),
    'date_field': 'pub_date',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'blog': BlogSitemap,
}






from ddtcms import settings

urlpatterns = patterns('',
    # Example:
    # (r'^ddtcms/', include('ddtcms.foo.urls')),
    (r'^',                     include('ddtcms.home.urls')),
    (r'^(?i)news/',            include('ddtcms.news.urls')),
    (r'^(?i)faq/',             include('ddtcms.faq.urls')),
    (r'^(?i)polls/',           include('ddtcms.polls.urls')),
    (r'^(?i)blog/',            include('ddtcms.blog.urls')),
    (r'^(?i)captcha/',         include('ddtcms.captcha.urls')),
    (r'^(?i)notice/',          include('ddtcms.notice.urls')),
    (r'^(?i)link/',            include('ddtcms.link.urls')),
    (r'^(?i)guestbook/',       include('ddtcms.guestbook.urls')),
    
    (r'^(?i)member/',          include('ddtcms.member.urls')),
    (r'^(?i)member/$',         direct_to_template, {'extra_context': { 'profiles': get_profiles }, 'template': 'member/front.html' }),

    (r'^(?i)photologue/',      include('photologue.urls')),
    #(r'^(?i)photologue/$',     direct_to_template, {'template': 'photologue/index.html' }),


    (r'^(?i)tags/',            include('tagging.urls')),
    

    # serve static medias
    (r'^(?i)media/(?P<path>.*)$',      'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    
    	    
    (r'^(?i)sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),    
    (r'^(?i)sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
    # user django comments system    
    (r'^(?i)comments/', include('django.contrib.comments.urls')),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    (r'^grappelli/',include('grappelli.urls')), 

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve',{'document_root':settings.STATIC_ROOT}),
    )