# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: forms.py
# Creation Date: 2011-11-04  16:19
# Last Modified: 2011-11-12 18:34:24
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django import forms
from django.forms import FileInput
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
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



class DynamicMultipleFileField(FileInput):

    #class Media:
    #    js = ("%seditor/nicEdit/nicEdit.js" % settings.MEDIA_URL,)

    def __init__(self,  attrs=None): 
        self.attrs = {'class': 'DynamicMultipleFileField','size':'50'}       
        if attrs is not None:
            self.attrs.update(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DynamicMultipleFileField, self).render(name, value, attrs)
        context = {
            'name': name,
        }
        return rendered  + mark_safe(render_to_string('editor/danamicmutiplefilefield.html', context))