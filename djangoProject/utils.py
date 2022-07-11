import django
import os
import random
import cv2
import base64

from django.core.mail import send_mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
django.setup()

X = 1


# 生成随机数
def generate_code():
    a = 0
    str = ''
    while a < 4:
        b = random.randint(0, 9)
        print(b)
        tem = '%d' % b
        str += tem
        a += 1

    print(str)
    return str


# 发送邮件
def send_email(email):
    ecode = generate_code()
    send_mail('SmartPension注册验证', '亲爱的的用户' + email + ',您的验证码是' + ecode, '2539496792@qq.com',
              [email], fail_silently=False)
    return ecode


# 将头像用base64编码
def encode_base64(path):
    # 通过opencv转base64
    img_im = cv2.imread(path)
    aa = base64.b64encode(cv2.imencode('.jpg', img_im)[1]).decode()
    coded = "data:image/jpg;base64,"+aa

    return coded


# 拍摄头像
def test():
    print("in test")
    cam = cv2.VideoCapture(0)  # 调用默认摄像头
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        # waitKey(1)持续等待
        cv2.waitKey(1)
        # 加一个鼠标点击事件，frame传给了OnMouseAction的param
        cv2.setMouseCallback("test", OnMouseAction, frame)
        global X
        if X == 2:
            X = 1
            break

    cam.release()
    cv2.destroyAllWindows()


def OnMouseAction(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # cv2.EVENT_LBUTTONDOWN 左键点击
        cv2.imwrite("C:/Users/user/PycharmProjects/EldersCare/profiles/youtemp.png", param)
        # 写进该目录，后面必须加上文件名（png,jpg格式），不需要提前创建空文件
        global X
        X = 2


