import cv2
from django.contrib.auth.hashers import make_password, check_password
from .models import AdminInfo, EventInfo

import json
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import send_email, encode_base64


def playback(camera):
    while True:
        # 读取图片
        ret, frame = camera.read()

        ret, frame = cv2.imencode('.jpeg', frame)
        if ret:
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@csrf_exempt
def fornow(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        camera = cv2.VideoCapture("events/invade.mp4")
        # camera = cv2.VideoCapture(0)
        # 使用流传输传输视频流
        return StreamingHttpResponse(playback(camera, id),
                                     content_type='multipart/x-mixed-replace; boundary=frame')


def invade_playback(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        camera = cv2.VideoCapture("events/" + id + "_invade.mp4")
        # 使用流传输传输视频流
        return StreamingHttpResponse(playback(camera),
                                     content_type='multipart/x-mixed-replace; boundary=frame')


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

        dic['status'] = "Success"
        encry_password = make_password(password)
        newAdmin = AdminInfo(email=email, password=encry_password,
                             status=1)
        print("before")
        newAdmin.save()
        print("after")

        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))

    if admin is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))


# 发送验证码（注册or忘记-重置密码）
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
        dic['code'] = ecode
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))


# 忘记密码，重置密码
@csrf_exempt
def forget_changePwd(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        print(post_content)
        email = post_content['email']
        new_pwd = post_content['newPwd']

        admin = AdminInfo.objects.get(email=email)
        admin.password = make_password(new_pwd)
        print(admin.password)
        admin.save()
        dic['status'] = "Success"

        print(dic)
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))


# 发送验证码(修改密码)
@csrf_exempt
def send_code_changePwd(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        admin_id = post_content['id']
        admin = AdminInfo.objects.get(id=admin_id)
        email = admin.email
        # 发送给邮箱的验证码
        global pcode
        pcode = ''
        pcode = send_email(email)

        dic['status'] = "Success"
        dic['code'] = pcode
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
        admin_id = post_content['id']
        new_pwd = post_content['newPwd']

        admin = AdminInfo.objects.get(id=admin_id)
        admin.password = make_password(new_pwd)
        print(admin.password)
        admin.save()
        dic['status'] = "Success"

        print(dic)
        return HttpResponse(json.dumps(dic))
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))


# 登录
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
        dic['id'] = admin.id
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


# 获取管理员详细信息
@csrf_exempt
def get_detail(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    # post请求返回对应详情
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
    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


# 获取所有事件
@csrf_exempt
def get_event(request):
    dic = {}
    if request.method == 'GET':
        events = EventInfo.objects.all()
        # 当没有任何记录
        if events.count() == 0:
            dic = {'status': "Failed", 'message': "no elderly"}
            return HttpResponse(json.dumps(dic))

        array = []
        orderedE = events.order_by('id')  # 将事件按id顺序排序
        eventType = ['摔倒', '情绪良好', '情绪低落', '义工交互', '禁止入侵']  # 事件类型
        for event in orderedE:
            print(event.images)
            if event.status == 5:
                image = '0'
            else:
                image = encode_base64(event.images)  # 将图片用base64编码

            time = json.dumps(event.createTime, default=str)[1:20]

            tmp = {'id': event.id,
                   'date': time,
                   'location': event.monitorID,
                   'description': event.description,
                   'type': eventType[event.status - 1],
                   'image': image  # 图片base64编码（除入侵检测-回放视频）
                   }
            array.append(tmp)
        dic = {"status": "success", "elderly_array": array}

        return HttpResponse(json.dumps(dic, ensure_ascii=False))
    else:
        dic['status'] = "Failed"
        dic['message'] = "Wrong request"
        return HttpResponse(json.dumps(dic))
