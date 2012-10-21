#coding=utf-8
from django import forms
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from captcha.models import CaptchaRequest
from captcha.examples import generate_sum_captcha
from random import random

class CaptchaInput(forms.widgets.Widget):
    """the widget for captcha input
    """
    input_type = 'text'
    def render(self, name, value, attrs=None):
        #generate captcha here!
        captcha = generate_sum_captcha()
        img = '<img src="/captcha/%s.jpg" align="absbottom" />' % captcha.uid
        hidden = '<input type="hidden" name="captcha_uid" value="%s" />' % captcha.uid

        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value:
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'%s%s<input%s />' %
                (img, hidden, forms.util.flatatt(final_attrs)))

class CaptchaUID(forms.widgets.Widget):
    """the widget for captcha input
    """
    input_type = 'hidden'
    is_hidden = True
    
    input_type = 'text'
    def render(self, name, value, attrs=None):
        #generate captcha here!
        return u''

def validate_captcha(form):
    cta = form.cleaned_data.get('captcha', '')
    uid = form.cleaned_data.get('captcha_uid', '')
    if not CaptchaRequest.validate(uid, cta):
        raise forms.ValidationError('输入的验证码有误，请重新输入')
    return cta


