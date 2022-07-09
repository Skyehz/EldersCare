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


# 发送验证码
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


# 修改密码
@csrf_exempt
def change_pwd(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        admin_id = post_content['admin_id']
        new_pwd = post_content['password']
        admin = AdminInfo.objects.get(id=admin_id)
        admin.password = new_pwd
        admin.save()
        dic['status'] = "Success"
        dic['admin_id'] = admin.id
        print(dic)
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        email = post_content['email']
        password = post_content['password']
        admin = AdminInfo.objects.get(email=email)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except AdminInfo.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Email"
        return HttpResponse(json.dumps(dic))
    if check_password(password, admin.password):
        dic['status'] = "Success"
        dic['admin_id'] = admin.id
        print(dic)
        return HttpResponse(json.dumps(dic))
    else:
        dic['message'] = "Wrong Password"
        dic['status'] = "Failed"
        print(dic)
        return HttpResponse(json.dumps(dic))


# 编辑系统管理员
@csrf_exempt
def edit_admin_info(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    # 解析前端的json数据建数据库记录
    post_content = json.loads(request.body)
    id = post_content['id']
    name = post_content['name']
    gender = post_content['gender']
    phone = post_content['phone']
    idCardNum = post_content['idCardNum']
    birthday = post_content['birthday']
    profilePath = post_content['profilePath']
    description = post_content['description']
    # 更新数据表记录
    AdminInfo.objects.filter(id=id).update(name=name, gender=gender,
                                           phone=phone, idCardNum=idCardNum,
                                           birthday=birthday, profilePath=profilePath,
                                           description=description, status=1)
    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))

