from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta
from random import random
from captcha.settings import TIMEOUT
import sha

def future_datetime(**kw_args):
    def on_call():
        return datetime.now()+timedelta(**kw_args)
    return on_call

class CaptchaRequest(models.Model):
    """
    A Captcha request, used to avoid spamming in comments and such
    Each request is valid for 15 minutes (you can change the value in the valid_until field)
    """
    valid_until = models.DateTimeField(default=future_datetime(minutes=TIMEOUT))
    answer = models.IntegerField()
    request_path = models.CharField(max_length=50, blank=True)
    uid = models.CharField(max_length=40, blank=True)
    text = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = _('CaptchaRequest')
        verbose_name_plural = _('CaptchaRequests')

    def save(self):
        shaobj = sha.new()
        # You can add anything you want here, if you're *really* serious
        # about an UID. This should be enough though
        shaobj.update(self.request_path)
        shaobj.update(str(random()))
        shaobj.update(str(datetime.now()))
        shaobj.update(str(self.valid_until))
        shaobj.update(str(self.answer))
        self.uid = shaobj.hexdigest()
        super(CaptchaRequest,self).save()

    @staticmethod
    def clean_expired():
        [x.delete() for x in CaptchaRequest.objects.filter(valid_until__lt=datetime.now())]

    @staticmethod
    def validate(request_uid, given_answer):
        result_list = CaptchaRequest.objects.filter(uid=request_uid)
        result = None
        if len(result_list) > 0:
            result = result_list[0]

        if not result:
            return False

        if result.valid_until < datetime.now():
            result.delete()
            return False

        if str(result.answer) != str(given_answer):
            result.delete()
            return False

        result.delete()
        return True

    @staticmethod
    def generate_request(text, answer, request_path='any'):
        """
        Generate a new captcha request. This creates 
        """
        captcha = CaptchaRequest(text=text, request_path=request_path, answer=answer)
        captcha.save()
        return captcha

