from .utils import test

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_elderly_record(request):
    dic = {}
    # 如果是get请求，看看之前有没有完善过信息
    if request.method == 'GET':
        try:
            post_content = json.loads(request.body)
            id = post_content['id']
            admin = AdminInfo.objects.get(id=id)
            dic['name'] = admin.name
            dic['gender'] = admin.gender
            dic['phone'] = admin.phone
            dic['idCardNum'] = admin.idCardNum
            dic['birthday'] = admin.birthday
            dic['description'] = admin.description
        except (KeyError, json.decoder.JSONDecodeError):
            dic['status'] = "Failed"
            dic['message'] = "No Input"
            return HttpResponse(json.dumps(dic))
        # dic['status'] = "Failed"
        # dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    # 解析前端的json数据建数据库记录
    try:
        post_content = json.loads(request.body)
        id = post_content['id']
        name = post_content['name']
        gender = post_content['gender']
        phone = post_content['phone']
        idCardNum = post_content['idCardNum']
        birthday = post_content['birthday']
        description = post_content['description']
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    # 更新数据表记录
    AdminInfo.objects.filter(id=id).update(name=name, gender=gender,
                                           phone=phone, idCardNum=idCardNum,
                                           birthday=birthday,
                                           description=description, status=1)
    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))

