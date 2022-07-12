from .utils import encode_base64
from .models import ElderlyInfo
from .models import AdminInfo
from .models import VolunteerInfo
from .video import capture_image

import json
import datetime
import os
import cv2
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_volunteer_info(request):
    dic = {}
    # 如果是get请求，错误
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    # 解析前端的json数据建数据库记录
    try:
        post_content = json.loads(request.body)
        name = post_content['name']
        gender = post_content['gender']
        phone = post_content['phone']
        idCardNum = post_content['idCardNum']
        birthday = post_content['birthday']
        hireDate = post_content['hireDate']
        dismissDate = post_content['dismissDate']
        description = post_content['description']
        createTime = datetime.datetime.now().strftime("%Y-%m-%d")
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    # 存储数据表记录
    new_volunteer = VolunteerInfo(name=name, gender=gender, phone=phone,
                                  idCardNum=idCardNum, birthday=birthday,
                                  hireDate=hireDate, dismissDate=dismissDate,
                                  description=description, createTime=createTime,
                                  status=1)
    new_volunteer.save()
    # 建立图片训练集目录
    imageSetDir = "/usr/local/djangoProject/imageSet/volunteer/"+str(new_volunteer.id)
    profilePath = "/usr/local/djangoProject/profiles/volunteer/"+str(new_volunteer.id)+".png"
    imageSetDir2 = "C:/Users/user/PycharmProjects/EldersCare/imageSet/volunteer/"+str(new_volunteer.id)
    # profilePath = "C:/Users/user/PycharmProjects/EldersCare/profiles/volunteer/"+str(new_volunteer.id)+".png"
    os.mkdir(imageSetDir2)
    VolunteerInfo.objects.filter(id=new_volunteer.id).update(imageSetDir=imageSetDir,
                                                             profilePath=profilePath)
    dic['status'] = "Success"
    dic['volunteer_id'] = new_volunteer.id
    return HttpResponse(json.dumps(dic))


# 拍摄义工头像
@csrf_exempt
def shot_volunteer_profile(request):
    dic = {}
    # get请求后端向前端推流
    if request.method == 'POST':
        try:
            content = json.loads(request.body)
            volunteer_id = content['volunteer_id']
        except (KeyError, json.decoder.JSONDecodeError):
            dic['status'] = "Failed"
            dic['message'] = "No Input"
            return HttpResponse(json.dumps(dic))
        camera = cv2.VideoCapture("rtmp://39.107.230.98:1935/live/home")
        # 使用流传输传输视频流
        return StreamingHttpResponse(capture_image(camera, "volunteer", volunteer_id),
                                     content_type='multipart/x-mixed-replace; boundary=frame')


# 显示全部老人信息
@csrf_exempt
def show_all_volunteer(request):
    dic = {}
    if request.method == 'GET':
        volunteers = VolunteerInfo.objects.all()
        # 当没有任何记录
        if volunteers.count() == 0:
            dic = {'status': "Failed", 'message': "no volunteer"}
            return HttpResponse(json.dumps(dic))

        array = []
        ordered = volunteers.order_by('id')  # 将老人记录按id顺序排序
        for volunteer in ordered:
            profile = encode_base64(volunteer.profilePath)  # 将图片用base64编码
            tmp = {'id': volunteer.id, 'name': volunteer.name, 'gender': volunteer.gender,
                   'phone': volunteer.phone, 'birthday': volunteer.birthday,
                   'description': volunteer.description, 'idCardNum': volunteer.idCardNum,
                   'hireDate': volunteer.hireDate, 'dismissDate': volunteer.dismissDate,
                   'profile': profile}
            array.append(tmp)
        dic = {"status": "success", "volunteer_array": array}

        return HttpResponse(json.dumps(dic, ensure_ascii=False))


# 修改义工信息
@csrf_exempt
def edit_volunteer(request):
    dic = {}
    # 如果是get请求，返回老人之前的信息
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        volunteer_id = post_content['id']  # 义工的id!
        name = post_content['name']
        gender = post_content['gender']
        phone = post_content['phone']
        idCardNum = post_content['idCardNum']
        birthday = post_content['birthday']
        description = post_content['description']
        hireDate = post_content['hireDate']
        dismissDate = post_content['dismissDate']

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    # 修改义工信息
    VolunteerInfo.objects.filter(id=volunteer_id).\
        update(name=name, gender=gender, phone=phone,
               idCardNum=idCardNum, birthday=birthday,
               hireDate=hireDate, dismissDate=dismissDate,
               description=description)

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


# 删除义工
@csrf_exempt
def delete_volunteer(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        id = post_content['id']
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))

    volunteer = VolunteerInfo.objects.get(id=id)
    volunteer.delete()

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


