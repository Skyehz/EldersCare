from django.contrib.auth.hashers import make_password, check_password
from .models import asdf

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
def register(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        print(username)
        user = asdf.objects.get(username=username)
    except asdf.DoesNotExist:
        dic['status'] = "Success"
        now = datetime.datetime.now()
        encry_password = make_password(password)
        newUser = asdf(username=username, password=encry_password,
                       time_created=now, last_login=now)
        newUser.save()
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))

    if user is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))