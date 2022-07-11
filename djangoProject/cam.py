import argparse
from datetime import datetime
import cv2
import imutils

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import tensorflow as tf
import numpy as np
import cv2

graph = tf.get_default_graph()
# 全局变量
from djangoProject.faceutildlib import FaceUtil

facial_recognition_model_path = 'models/face_recognition_hog.pickle'
model_path = 'models/face_expression.hdf5'

# 全局常量
FACIAL_EXPRESSION_TARGET_WIDTH = 28
FACIAL_EXPRESSION_TARGET_HEIGHT = 28

model = tf.keras.models.load_model(model_path)
faceutil = FaceUtil(facial_recognition_model_path)


class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture("rtmp://39.107.230.98:1935/live/home")
        # self.cap = cv2.VideoCapture(0)
        self.count = 1
        self.timeF = 2
    def __del__(self):
        self.cap.release()

    # 处理画面（画警戒区域等等）
    def get_frame(self):
        success, image = self.cap.read()
        self.count = self.count+1
        if not success:
            return
        image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        # if self.count % self.timeF != 0:
        #     print("Don't classify")
        #     ret, jpeg = cv2.imencode('.jpeg', image)
        #     return jpeg.tobytes()
        # print("Classify")

        # 每隔timeF帧进行识别操作
        # image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        # image = imutils.resize(image, width=600)

        # 标注左上角的时间
        datet = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(image, datet, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2, cv2.LINE_AA)  # cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, 8


        face_location_list, names = faceutil.get_face_location_and_name(
            image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # loop over the faces bounding boxes
        for ((left, top, right, bottom), name) in zip(
                face_location_list,
                names):

            roi = gray[top:bottom, left:right]
            roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH,
                                   FACIAL_EXPRESSION_TARGET_HEIGHT))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # determine facial expression
            # (neural, smile) = model.predict(roi)[0]
            global graph
            with graph.as_default():
                (neural, smile) = model.predict(roi)[0]

            label = "Neural" if neural > smile else "Smile"

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(image, name + " is" + label, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(image, (left, top), (right, bottom),
                          (0, 0, 255), 2)

        # show our detected faces along with smiling/not smiling labels
        ret, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()
        # else:
        #     print("wrong read")
