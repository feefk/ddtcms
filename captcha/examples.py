from captcha.models import CaptchaRequest
from random import random

def generate_sum_captcha(request_path='any'):
    numbers = (int(random()*9)+1,int(random()*9)+1)
    text = "%d+%d=" % numbers
    answer = sum(numbers)
    return CaptchaRequest.generate_request(text, answer, request_path)

