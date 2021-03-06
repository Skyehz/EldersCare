import cv2
import time
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from djangoProject.cam import VideoCamera


def capture_image(camera, type, id):
    # path 可以修改
    path = "/usr/local/djangoProject/profiles/"+type+"/"+str(id)+".png"
    print(path)
    tik = time.time()  # 开始记时
    while True:
        # 读取图片
        ret, frame = camera.read()
        if ret:
            tok = time.time()
            if tok - tik >= 5:
                cv2.imwrite(path, frame)
                print("ok")
                break
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            if ret:
                # 转换为byte类型的，存储在迭代器中
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
            # tok = time.time()
            # if tok-tik >= 5:
            #     cv2.imwrite(path, frame)
            #     print("ok")
            #     break


# def gen_display(camera):
#     """
#     视频流生成器功能。
#     """
#     while True:
#         # 读取图片
#         ret, frame = camera.read()
#         if ret:
#             frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#             # 将图片进行解码
#             ret, frame = cv2.imencode('.jpeg', frame)
#             if ret:
#                 # 转换为byte类型的，存储在迭代器中
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def gen_display(camera):

    while True:
        frame = camera.get_frame(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@csrf_exempt
def video(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象"
    # camera = cv2.VideoCapture(0)
    # camera = cv2.VideoCapture("rtmp://39.107.230.98:1935/live/home")
    # 使用流传输传输视频流
    return StreamingHttpResponse(gen_display(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

