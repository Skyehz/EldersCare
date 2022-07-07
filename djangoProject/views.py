from django.contrib.auth.hashers import make_password, check_password
from .models import AdminInfo

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import send_email


@csrf_exempt
def register(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        email = post_content['email']
        password = post_content['password']
        code = post_content['code']
        admin = AdminInfo.objects.get(email=email)
    except AdminInfo.DoesNotExist:
        if code == ecode:

            dic['status'] = "Success"
            encry_password = make_password(password)
            newAdmin = AdminInfo(email=email, password=encry_password,
                             status=1)
            newAdmin.save()
        else:
            dic['status'] = "Failed"
            dic['message'] = "Wrong code"
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))

    if admin is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def send_code(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        email = post_content['email']
        # 发送给邮箱的验证码
        global ecode
        ecode = ''
        ecode = send_email(email)

        dic['status'] = "Success"

        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))