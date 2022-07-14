import _thread
import argparse
import os
import shutil
import time

from oldcare.facial import FaceUtil
from PIL import Image, ImageDraw, ImageFont
import cv2

# 全局参数
# audio_dir = './audios'

# 传入参数
# ap = argparse.ArgumentParser()
# ap.add_argument("-ic", "--id", required=True, help="")
# ap.add_argument("-id", "--imagedir", required=True, help="")
# args = vars(ap.parse_args())

action_list = ['blink', 'open_mouth', 'smile', 'rise_head', 'bow_head',
               'look_left', 'look_right']
action_map = {'blink': '请眨眼', 'open_mouth': '请张嘴',
              'smile': '请笑一笑', 'rise_head': '请抬头',
              'bow_head': '请低头', 'look_left': '请看左边',
              'look_right': '请看右边'}

faceutil = FaceUtil()


class CaptureCamera(object):
    def __init__(self, type, elderly_id):
        self.cam = cv2.VideoCapture("rtmp://39.107.230.98:1935/live/collect")
        # self.cam = cv2.VideoCapture(0)
        self.type = type
        self.elderly_id = elderly_id
        # 不断循环
        self.counter = 0
        self.error = 0
        self.start_time = None
        self.limit_time = 2  # 2 秒

    def __del__(self):
        self.cam.release()

    # 判断是否可以检测
    def prepare(self):
        while True:
            self.counter += 1
            _, image = self.cam.read()
            if self.counter <= 10:  # 放弃前10帧
                continue
            image = cv2.flip(image, 1)

            if self.error == 1:
                self.end_time = time.time()
                difference = self.end_time - self.start_time
                print(difference)
                if difference >= self.limit_time:
                    self.error = 0

            face_location_list = faceutil.get_face_location(image)
            for (left, top, right, bottom) in face_location_list:
                cv2.rectangle(image, (left, top), (right, bottom),
                              (0, 0, 255), 2)

            face_count = len(face_location_list)
            if self.error == 0 and face_count == 0:  # 没有检测到人脸
                print('[WARNING] 没有检测到人脸')
                # audioplayer.play_audio(os.path.join(audio_dir,
                #                                     'no_face_detected.mp3'))
                self.error = 1
                self.start_time = time.time()
            elif self.error == 0 and face_count == 1:  # 可以开始采集图像了
                print('[INFO] 可以开始采集图像了')
                # audioplayer.play_audio(os.path.join(audio_dir,
                #                        'start_image_capturing.mp3'))
                break
            elif self.error == 0 and face_count > 1:  # 检测到多张人脸
                print('[WARNING] 检测到多张人脸')
                # audioplayer.play_audio(os.path.join(audio_dir,
                #                        'multi_faces_detected.mp3'))
                self.error = 1
                self.start_time = time.time()
            else:
                pass

    # 处理画面
    def get_frame(self):
        _, image = self.cam.read()
        if not _:
            print("空frame")
            return

        # 算法部分

        # 开始采集人脸
        for action in action_list:
            # audioplayer.play_audio(os.path.join(audio_dir,action+'.mp3'))
            time.sleep(2)
            action_name = action_map[action]

            cv2.putText(image, action_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2, cv2.LINE_AA)  # cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, 8

            self.counter = 1
            for i in range(15):
                print('%s-%d' % (action_name, i))
                # image = cv2.flip(image, 1)
                # origin_img = image.copy()  # 保存时使用
                #
                face_location_list = faceutil.get_face_location(image)
                for (left, top, right, bottom) in face_location_list:
                    cv2.rectangle(image, (left, top),
                                  (right, bottom), (0, 0, 255), 2)

                # img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                #
                # draw = ImageDraw.Draw(img_PIL)
                # draw.text((int(image.shape[1] / 2), 30), action_name,
                #           font=ImageFont.truetype('NotoSansCJK-Black.ttc', 40),
                #           fill=(255, 0, 0))  # linux

                # # 转换回OpenCV格式
                # image = cv2.cvtColor(np.asarray(img_PIL),
                #                           cv2.COLOR_RGB2BGR)
                #
                # cv2.imshow('Collecting Faces', image)  # show the image
                # 线程储存图片
                # _thread.start_new_thread(writeImg, (self.type, action, self.counter, origin_img, self.elderly_id))
                path = "/usr/local/djangoProject/imageSet/" + self.type + "/" + str(self.elderly_id)
                image_name = os.path.join(path, action + '_' + str(self.counter) + '.jpg')
                cv2.imwrite(image_name, image)

                self.counter += 1
                # image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

                ret, jpeg = cv2.imencode('.jpeg', image)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        # 结束
        print('[INFO] 采集完毕')
        # audioplayer.play_audio(os.path.join(audio_dir,'end_capturing.mp3'))


def writeImg(type, action, counter, origin_img, elderly_id):
    path = "/usr/local/djangoProject/imageSet/" + type + "/" + str(elderly_id)
    image_name = os.path.join(path, action + '_' + str(counter) + '.jpg')
    cv2.imwrite(image_name, origin_img)
