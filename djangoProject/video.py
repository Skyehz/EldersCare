import cv2
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt


def gen_display(camera):
    """
    视频流生成器功能。
    """
    while True:
        # 读取图片
        ret, frame = camera.read()
        if ret:
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            if ret:
                # 转换为byte类型的，存储在迭代器中
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@csrf_exempt
def video(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象"
    camera = cv2.VideoCapture('rtmp://192.168.43.217:1935/live/home')
    # camera = cv2.VideoCapture(0)
    # 使用流传输传输视频流
    return StreamingHttpResponse(gen_display(camera), content_type='multipart/x-mixed-replace; boundary=frame')

#
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
