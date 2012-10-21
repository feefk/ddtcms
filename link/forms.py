# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: forms.py
# Creation Date: 2011-11-05  12:58
# Last Modified: 2011-11-12 17:13:35
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django import forms
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

class CreateLinkForm(forms.Form):
    title = forms.CharField(label=_("Title"), max_length=100)
    url  = forms.CharField(label=_("Url"), max_length=255)
    description = forms.CharField(label=_("Description"), required=False,widget=forms.Textarea(attrs={'rows':8, 'cols':50}))
    
    def clean_url(self):
        if 'url' in self.cleaned_data:
            url=self.cleaned_data['url']
            if url.startswith("http"):
                return url
        raise forms.ValidationError("Invalid url, must begin with `http`")

class CGPUploadForm(forms.Form):
    cgpfile     = forms.FileField(label=_("Please Choose GreenBrowser Group Files(*.cgp)"), max_length=100)
    title       = forms.CharField(label=_("Title"), max_length=100)
    category    = forms.CharField(label=_("Title"), max_length=100)
    description = forms.CharField(label=_("Description"), required=False,widget=forms.Textarea(attrs={'rows':8, 'cols':50}))
