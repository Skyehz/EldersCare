from .utils import test
from .models import ElderlyInfo
from .models import AdminInfo
from .models import FamilyInfo
from .models import FamilyElderlyRelationship

import json
import datetime
import os
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
    imageSetDir = "C:/Users/user/PycharmProjects/EldersCare/imageSet/elderly/"+str(newElderly.id)
    profilePath = "C:/Users/user/PycharmProjects/EldersCare/profiles/elderly/"+str(newElderly.id)+".png"
    os.mkdir(imageSetDir)
    ElderlyInfo.objects.filter(id=newElderly.id).update(imageSetDir=imageSetDir,
                                                        profilePath=profilePath)
    dic['status'] = "Success"
    dic['elderly_id'] = newElderly.id
    return HttpResponse(json.dumps(dic))


