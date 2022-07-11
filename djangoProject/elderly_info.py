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
    # imageSetDir = "/usr/local/djangoProject/imageSet/elderly/"+str(newElderly.id)
    # profilePath = "/usr/local/djangoProject/profiles/elderly/"+str(newElderly.id)+".png"
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
        for elderly in orderedE:
            print(elderly.profilePath)
            profile = encode_base64(elderly.profilePath)  # 将图片用base64编码
            # 获取家属
            relations = FamilyElderlyRelationship.objects.filter(elderlyId=elderly)
            famArray = []
            for r in relations:
                family = r.familyId
                tt = {'id': family.id, 'wechatId': family.wechatId, 'name': family.name, 'gender': family.gender,
                      'phone': family.phone, 'email': family.email}
                print(tt)
                famArray.append(tt)
                print(famArray)
            print(famArray)
            tmp = {'id': elderly.id, 'name': elderly.name, 'gender': elderly.gender,
                   'phone': elderly.phone, 'birthday': elderly.birthday,
                   'description': elderly.description, 'idCardNum': elderly.idCardNum,
                   'checkinDate': elderly.checkinDate, 'checkoutDate': elderly.checkoutDate,
                   'roomNum': elderly.roomNum, 'health': elderly.health,
                   'families': famArray, 'profile': profile}
            array.append(tmp)
        dic = {"status": "success", "elderly_array": array}

        return HttpResponse(json.dumps(dic, ensure_ascii=False))


# 修改老人信息
@csrf_exempt
def edit_elderly(request):
    dic = {}
    # 如果是get请求，返回老人之前的信息
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
        # content = json.loads(request.body)
        # id = content['id']
        # elderly = ElderlyInfo.objects.get(id=id)
        # profile = encode_base64(elderly.profilePath)  # 将图片用base64编码
        # # 获取家属
        # relations = FamilyElderlyRelationship.objects.filter(elderlyId=elderly)
        # famArray = []
        # for r in relations:
        #     family = r.familyId
        #     tt = {'wechatId': family.wechatId, 'name': family.name, 'gender': family.gender,
        #           'phone': family.phone, 'email': family.email}
        #     print(tt)
        #     famArray.append(tt)
        #
        # print(famArray)
        # dic = {'name': elderly.name, 'gender': elderly.gender,
        #        'phone': elderly.phone, 'birthday': elderly.birthday,
        #        'description': elderly.description, 'idCardNum': elderly.idCardNum,
        #        'checkinDate': elderly.checkinDate, 'checkoutDate': elderly.checkoutDate,
        #        'roomNum': elderly.roomNum, 'health': elderly.health,
        #        'families': famArray, 'profile': profile}
        #
        # return HttpResponse(json.dumps(dic, ensure_ascii=False))

    try:
        post_content = json.loads(request.body)
        elderly_id = post_content['id']  # 老人的id!
        name = post_content['name']
        gender = post_content['gender']
        phone = post_content['phone']
        idCardNum = post_content['idCardNum']
        birthday = post_content['birthday']
        description = post_content['description']
        print(description)
        checkinDate = post_content['checkinDate']
        checkoutDate = post_content['checkoutDate']
        roomNum = post_content['roomNum']
        health = post_content['health']
        families = post_content['families']
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    # 修改老人信息
    ElderlyInfo.objects.filter(id=elderly_id).update(name=name, gender=gender, phone=phone,
                                                     idCardNum=idCardNum, birthday=birthday,
                                                     checkinDate=checkinDate, checkoutDate=checkoutDate,
                                                     roomNum=roomNum, health=health, description=description)
    # 修改/新增家属信息
    for family in families:
        try:
            existed = FamilyInfo.objects.get(email=family['email'])
            # 更新记录
            FamilyInfo.objects.filter(email=family['email']).\
                update(wechatId=family['wechatId'], name=family['name'],
                       phone=family['phone'], email=family['email'],
                       gender=family['gender'])

        except FamilyInfo.DoesNotExist:
            # 如果没有这位家属，则是新增加的家属
            createTime = datetime.datetime.now().strftime("%Y-%m-%d")
            new_fam = FamilyInfo(wechatId=family['wechatId'], name=family['name'],
                                 phone=family['phone'], gender=family['gender'],
                                 email=family['email'], createTime=createTime, status=1)
            new_fam.save()
            # 新建关系表记录
            newRelation = FamilyElderlyRelationship(elderlyId=ElderlyInfo.objects.get(id=elderly_id),
                                                    familyId=new_fam, createTime=createTime, status=1)
            newRelation.save()

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


# 删除老人
@csrf_exempt
def delete_elderly(request):
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

    elderly = ElderlyInfo.objects.get(id=id)
    relations = FamilyElderlyRelationship.objects.filter(elderlyId=elderly)
    # 记录所有家属信息准备删除
    for r in relations:
        family = r.familyId
        r.delete()
        family.delete()
    elderly.delete()

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))




