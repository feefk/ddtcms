from django.contrib.sites.models import Site
import datetime
from ddtcms import get_version
from django import get_version as django_version
from django.core.cache import cache

from ddtcms import settings
from ddtcms.theme.models import get_current_theme


def site(request):
    """
    Adds site-related context variables to the context.
    """
    current_site = Site.objects.get_current()
    current_theme = get_current_theme()
    
    current_themename = "default"
    if current_theme:
        current_themename= current_theme.name

    return {
        'DJANGO_VERSION': django_version(),
        'DDTCMS_VERSION': get_version(),
        'SITE_NAME':      current_site.name,
        'SITE_DOMAIN':    current_site.domain,
        'SITE_URL':       "http://www.%s" % (current_site.domain),
        'SITE_TIME':      datetime.datetime.now(),
        'THEME_NAME':     current_themename,
        'DEBUG':          settings.DEBUG,
    }
