import django
import os
import random

from django.core.mail import send_mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
django.setup()


# 生成随机数
def generate_code():
    a = 0
    str = ''
    while a < 4:
        b = random.randint(0, 9)
        print(b)
        tem = '%d' % b
        str += tem
        a += 1

    print(str)
    return str


# 发送邮件
def send_email(email):
    ecode = generate_code()
    send_mail('SmartPension注册验证', '亲爱的的用户' + email + ',您的验证码是' + ecode, '2539496792@qq.com',
              [email], fail_silently=False)
    return ecode

