from .utils import test

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_elderly_record(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        name = post_content['name']
        gender = post_content['gender']
        phone = post_content['phone']
        idCardNum = post_content['idCardNum']
        birthday = post_content['birthday']
    except AdminInfo.DoesNotExist:
        if code == ecode:
            dic['status'] = "Success"
            encry_password = make_password(password)
            newAdmin = AdminInfo(email=email, password=encry_password,
                                 status=1)
            print("before")
            newAdmin.save()
            print("after")
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