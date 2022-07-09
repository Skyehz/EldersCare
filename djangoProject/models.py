from django.db import models
from django.utils import timezone


class asdf(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=30)
    time_created = models.DateTimeField(default=timezone.now())
    password = models.TextField()
    last_login = models.DateField(default=timezone.now())

    def __str__(self):
        return self.username


# 系统管理员信息表
class AdminInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(verbose_name='email', max_length=30, unique=True)  # 邮箱作为登录账号
    password = models.TextField()  # 在视图里加密
    name = models.CharField(verbose_name='name', max_length=40)  # 真实姓名
    gender = models.CharField(verbose_name='gender', max_length=2)  # f为女，m为男
    phone = models.CharField(verbose_name='phone', max_length=20)
    idCardNum = models.CharField(verbose_name='idCardNum', max_length=18)
    birthday = models.CharField(verbose_name='birthday', max_length=25)
    profilePath = models.CharField(verbose_name='profilePath', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 老人信息表
class ElderlyInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='name', max_length=40)
    gender = models.CharField(verbose_name='gender', max_length=2)  # f为女，m为男
    phone = models.CharField(verbose_name='phone', max_length=20)
    idCardNum = models.CharField(verbose_name='idCardNum', max_length=18)
    birthday = models.CharField(verbose_name='birthday', max_length=25)
    checkinDate = models.CharField(verbose_name='checkinDate', max_length=25)  # 登记入住时间
    checkoutDate = models.CharField(verbose_name='checkoutDate', max_length=25)
    imageSetDir = models.CharField(verbose_name='imageSetDir', max_length=255)
    profilePath = models.CharField(verbose_name='profilePath', max_length=255)
    roomNum = models.CharField(verbose_name='roomNum', max_length=10)
    health = models.CharField(verbose_name='health', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    createTime = models.DateTimeField(default=timezone.now())  # 记录创建时间
    createBy = models.ForeignKey(AdminInfo, on_delete=models.SET_NULL, null=True, related_name='createBy')  # 创建该记录的管理员
    updateTime = models.DateTimeField(null=True)  # 最近更新时间
    updateBy = models.ForeignKey(AdminInfo, on_delete=models.SET_NULL, null=True, related_name='updateBy')  # 最近更新的管理员
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 老人位置表
class ElderlyLocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    elderlyId = models.ForeignKey(ElderlyInfo, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=20)  # 经度
    latitude = models.CharField(max_length=20)  # 维度
    createTime = models.DateTimeField(default=timezone.now())
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 工作人员信息表
class EmployeeInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='name', max_length=40)
    gender = models.CharField(verbose_name='gender', max_length=2)  # f为女，m为男
    phone = models.CharField(verbose_name='phone', max_length=20)
    idCardNum = models.CharField(verbose_name='idCardNum', max_length=18)
    birthday = models.CharField(verbose_name='birthday', max_length=25)
    hireDate = models.CharField(verbose_name='checkinDate', max_length=25)  # 登记入住时间
    dismissDate = models.CharField(verbose_name='checkoutDate', max_length=25, blank=True)
    imageSetDir = models.CharField(verbose_name='imageSetDir', max_length=255)
    profilePath = models.CharField(verbose_name='profilePath', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    createTime = models.DateTimeField(default=timezone.now())  # 记录创建时间
    createBy = models.ForeignKey(AdminInfo, on_delete=models.SET_NULL, null=True, related_name='creator')  # 创建该记录的管理员
    updateTime = models.DateTimeField(null=True)  # 最近更新时间
    updateBy = models.ForeignKey(AdminInfo, on_delete=models.SET_NULL, null=True, related_name='updater')  # 最近更新的管理员
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 事件等级表
class EventLevel(models.Model):
    id = models.BigAutoField(primary_key=True)
    levelName = models.CharField(verbose_name='levelName', max_length=20)
    description = models.CharField(verbose_name='description', max_length=255)
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 事件类型表
class EventType(models.Model):
    id = models.BigAutoField(primary_key=True)
    typeName = models.CharField(verbose_name='typeName', max_length=20)
    description = models.CharField(verbose_name='description', max_length=255)
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 事件信息表
class EventInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    typeId = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True)  # 事件类型id
    levelId = models.ForeignKey(EventLevel, on_delete=models.SET_NULL, null=True)  # 事件等级id
    createTime = models.DateTimeField(default=timezone.now())
    handleTime = models.DateTimeField()
    monitorID = models.CharField(max_length=20)  # 监控摄像头id
    images = models.CharField(max_length=2048)  # 照片地址
    description = models.CharField(verbose_name='description', max_length=255)
    elderly = models.ForeignKey(ElderlyInfo, on_delete=models.CASCADE)
    isHandled = models.IntegerField()  # 0未处理，1处理
    status = models.IntegerField()  # 数据是否有效，0无效1有效
    relatedID = models.CharField(max_length=500)  # 事件相关人员id


# 家属基本信息表
class FamilyInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    wechatId = models.CharField(max_length=50)  # 微信号
    name = models.CharField(verbose_name='name', max_length=40)
    gender = models.CharField(verbose_name='gender', max_length=2)  # f为女，m为男
    phone = models.CharField(verbose_name='phone', max_length=20)
    email = models.EmailField(verbose_name='email', max_length=20, unique=True)
    createTime = models.DateTimeField(default=timezone.now())  # 记录创建时间
    updateTime = models.DateTimeField(null=True)  # 最近更新时间
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 家属和老人关系表
class FamilyElderlyRelationship(models.Model):
    id = models.BigAutoField(primary_key=True)
    elderlyId = models.ForeignKey(ElderlyInfo, on_delete=models.CASCADE)
    familyId = models.ForeignKey(FamilyInfo, on_delete=models.CASCADE)
    createTime = models.DateTimeField(default=timezone.now())  # 记录创建时间
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 监控信息表
class Monitor(models.Model):
    id = models.BigAutoField(primary_key=True)
    createTime = models.DateTimeField(default=timezone.now())  # 记录创建时间
    updateTime = models.DateTimeField(null=True)  # 最近更新时间
    status = models.IntegerField()  # 数据是否有效，0无效1有效
    description = models.CharField(verbose_name='description', max_length=255)
    ip = models.CharField(max_length=255)


# 视频信息表
class Video(models.Model):
    id = models.BigAutoField(primary_key=True)
    monitorId = models.ForeignKey(Monitor, on_delete=models.SET_NULL, null=True)
    locationURL = models.CharField(max_length=255)  # 视频地址
    beginTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.IntegerField()  # 数据是否有效，0无效1有效


# 义工信息表
class VolunteerInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='name', max_length=40)
    gender = models.CharField(verbose_name='gender', max_length=2)  # f为女，m为男
    phone = models.CharField(verbose_name='phone', max_length=20)
    idCardNum = models.CharField(verbose_name='idCardNum', max_length=18)
    birthday = models.CharField(verbose_name='birthday', max_length=25)
    hireDate = models.CharField(verbose_name='checkinDate', max_length=25)  # 登记入住时间
    dismissDate = models.CharField(verbose_name='checkoutDate', max_length=25, blank=True)
    imageSetDir = models.CharField(verbose_name='imageSetDir', max_length=255)
    profilePath = models.CharField(verbose_name='profilePath', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    createTime = models.DateTimeField(default=timezone.now())  # 记录创建时间
    updateTime = models.DateTimeField(null=True)  # 最近更新时间
    status = models.IntegerField()  # 数据是否有效，0无效1有效


