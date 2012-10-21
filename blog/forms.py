# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: forms.py
# Creation Date: 2011-11-12 13:46:32
# Last Modified: 2011-11-12 13:48:52
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#
# ------------------------------------------------------------

# django.
from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.blog.models import Blog
from ddtcms.blog.models import Category

from ddtcms.captcha.forms import *
from rte.kindeditor.widgets import KindEditor
# ------------------------------------------------------------

# config.
attrs_dict = { 'class': 'required' }

CATEGORY_CHOICES = {}
# ------------------------------------------------------------







class MyBlogAdminForm(forms.ModelForm):
    content   = forms.CharField(label=_(u"Content"), widget=KindEditor(attrs={'rows':15, 'cols':100}),required=True)          
    class Meta:
        model = Blog
        #widgets = {
        #    'content':KindEditor(),
        #}
        
class CreateBlogForm(forms.ModelForm):

    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'username'))
    title = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)),
                             label=_(u'title'))
                             
    #category = forms.ChoiceField(label=_(u'category'), choices=[(c.id,c.name) for c in Category.objects.all()])
    #category = forms.ModelChoiceField(label=_(u'category'), queryset=Category.objects.all())
    category = forms.ChoiceField(label=_(u'category'), choices=CATEGORY_CHOICES)
    
    
    pub_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs=attrs_dict),
                                label=_(u'datetime'))
                                
    content = forms.CharField(label=_(u'content'),widget=KindEditor())
    slug          = forms.SlugField(label=_(u'Slug'),help_text="Use English Or Pinyin.")
    summary       = forms.CharField(label=_(u'Summary'),help_text="One paragraph. Don't add tag.")
    #tags          = forms.MultipleChoiceField(label=u'tag', choices=[(t.id,t.name) for t in Tag.objects.all()])   
    tags          = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)), label=_(u'tags'))
    captcha_uid = forms.CharField(
            required=True,
            label="",
            max_length=40,
            widget=CaptchaUID)
    
    captcha = forms.CharField(
            required=True,
            label="confirm msg",
            max_length=1000,
            widget=CaptchaInput)
 
    class Meta:
        model = Blog

    def clean_captcha(self):
        return validate_captcha(self)
        
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    profile_callback=profile_callback)
        return new_user