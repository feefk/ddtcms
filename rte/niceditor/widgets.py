# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: widgets.py
# Creation Date: 2011-11-05  01:51
# Last Modified: 2011-11-12 18:34:1
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms import TextInput, Textarea
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


class NicEditor(Textarea):

    class Media:
        js = ("%seditor/nicEdit/nicEdit.js" % settings.MEDIA_URL,)

    def __init__(self,  attrs=None):
    	
        self.attrs = {'class': 'niceditor','cols':50}
        if attrs:
            self.attrs.update(attrs)
            #a=self.attrs
    	#debug()
        super(NicEditor, self).__init__(self.attrs)

    def render(self, name, value, attrs=None):
        rendered = super(NicEditor, self).render(name, value, attrs)
        context = {
            'name': name,
            'MEDIA_URL':settings.MEDIA_URL,
        }
        return rendered  + mark_safe(render_to_string(
            'editor/niceditor.html', context))