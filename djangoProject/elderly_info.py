from .utils import encode_base64
from .models import ElderlyInfo
from .models import AdminInfo
from .models import FamilyInfo
from .models import FamilyElderlyRelationship
from .video import capture_image

import json
import datetime
import os
import cv2
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, date


@csrf_exempt
def create_elderly_record(request):
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
        checkinDate = post_content['checkinDate']
        checkoutDate = post_content['checkoutDate']
        roomNum = post_content['roomNum']
        health = post_content['health']
        description = post_content['description']
        createTime = datetime.datetime.now().strftime("%Y-%m-%d")
        print(createTime)
        createBy = AdminInfo.objects.get(id=post_content['id'])
        families = post_content['families']
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    # 存储数据表记录
    newElderly = ElderlyInfo(name=name, gender=gender, phone=phone,
                             idCardNum=idCardNum, birthday=birthday,
                             checkinDate=checkinDate, checkoutDate=checkoutDate,
                             roomNum=roomNum, health=health,
                             description=description, createTime=createTime,
                             createBy=createBy, status=1)
    print(newElderly.createTime)
    newElderly.save()
    for family in families:
        print(family)
        # 家属相关信息
        wechatId = family['wechatId']
        family_name = family['name']
        family_gender = family['gender']
        family_phone = family['phone']
        email = family['email']
        newFamily = FamilyInfo(wechatId=wechatId, name=family_name,
                               phone=family_phone, gender=family_gender,
                               email=email, createTime=createTime, status=1)
        newFamily.save()
        # relatedE = ElderlyInfo.objects.get(id=newElderly.id)
        # relatedF = FamilyInfo.objects.get(id=newFamily.id)
        newRelation = FamilyElderlyRelationship(elderlyId=newElderly, familyId=newFamily,
                                                createTime=createTime, status=1)
        newRelation.save()
    imageSetDir = "C:/Users/user/PycharmProjects/EldersCare/imageSet/elderly/"+str(newElderly.id)
    profilePath = "C:/Users/user/PycharmProjects/EldersCare/profiles/elderly/"+str(newElderly.id)+".png"
    os.mkdir(imageSetDir)
    ElderlyInfo.objects.filter(id=newElderly.id).update(imageSetDir=imageSetDir,
                                                        profilePath=profilePath)
    dic['status'] = "Success"
    dic['elderly_id'] = newElderly.id
    return HttpResponse(json.dumps(dic))


# 拍摄老人头像
@csrf_exempt
def shot_elderly_profile(request):
    dic = {}
    # get请求后端向前端推流
    if request.method == 'GET':
        try:
            content = json.loads(request.body)
            elderly_id = content['elderly_id']
        except (KeyError, json.decoder.JSONDecodeError):
            dic['status'] = "Failed"
            dic['message'] = "No Input"
            return HttpResponse(json.dumps(dic))
        camera = cv2.VideoCapture("rtmp://39.107.230.98:1935/live/home")
        # 使用流传输传输视频流
        return StreamingHttpResponse(capture_image(camera, "elderly", elderly_id),
                                     content_type='multipart/x-mixed-replace; boundary=frame')


# 显示全部老人信息
@csrf_exempt
def show_all_elderly(request):
    dic = {}
    if request.method == 'GET':
        elderlys = ElderlyInfo.objects.all()
        # 当没有任何记录
        if elderlys.count() == 0:
            dic = {'status': "Failed", 'message': "no elderly"}
            return HttpResponse(json.dumps(dic))

        array = []
        orderedE = elderlys.order_by('id')  # 将老人记录按id顺序排序
        for elderly in orderedE:  # TODO: add photo using base64
            profile = encode_base64(elderly.profilePath)
            tmp = {'id': elderly.id, 'name': elderly.name, 'gender': elderly.gender,
                   'phone': elderly.phone, 'birthday': elderly.birthday,
                   'description': elderly.description, 'idCardNum': elderly.idCardNum,
                   'checkinDate': elderly.checkinDate, 'checkoutDate': elderly.checkoutDate,
                   'roomNum': elderly.roomNum, 'health': elderly.health, 'profile': profile}
            array.append(tmp)
        dic = {"status": "success", "elderly_array": array}

        return HttpResponse(json.dumps(dic, ensure_ascii=False))


# 修改老人信息






