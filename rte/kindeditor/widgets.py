# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: widgets.py
# Creation Date: 2011-10-28  05:42
# Last Modified: 2011-11-12 18:33:40
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
#from models import MODEL
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------



class KindEditor(forms.Textarea):

    class Media:
        css = {
              'all': (  settings.MEDIA_URL + 'editor/kindeditor-4.0.1/themes/default/default.css',
                        settings.MEDIA_URL + 'editor/kindeditor-4.0.1/plugins/code/prettify.js',),
        }
        js  = (
                "%seditor/kindeditor-4.0.1/kindeditor.js" % settings.MEDIA_URL,
                settings.MEDIA_URL + 'editor/kindeditor-4.0.1/plugins/code/prettify.js',
        )

    def __init__(self, attrs = {}):
        attrs['rel']   = 'kind'
        #attrs['style'] = "width:800px;height:400px;visibility:hidden;"
        #attrs['cols']  = 50
        super(KindEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(KindEditor, self).render(name, value, attrs)
        context = {
            'name': name,
            'MEDIA_URL':settings.MEDIA_URL,
        }
        return rendered  + mark_safe(render_to_string('editor/kindeditor.html', context))