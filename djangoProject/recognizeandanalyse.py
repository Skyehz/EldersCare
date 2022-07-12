# -*- coding: utf-8 -*-
'''
测试表情识别模型

用法：
python testingfacialexpression.py
python testingfacialexpression.py --filename tests/room_04.avi
'''

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import tensorflow as tf
from oldcare.facial import FaceUtil
import numpy as np
import imutils
import cv2
import time
import argparse

# 传入参数
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=False, default='',
                help="")
args = vars(ap.parse_args())

# 全局变量
facial_recognition_model_path = 'models/face_recognition_hog.pickle'
model_path = 'models/face_expression.hdf5'
input_video = args['filename']

# 全局常量
FACIAL_EXPRESSION_TARGET_WIDTH = 28
FACIAL_EXPRESSION_TARGET_HEIGHT = 28

# load the faces detector cascade and smile detector CNN
# model = load_model(model_path)
model = tf.keras.models.load_model(model_path)

# if a videos path was not supplied, grab the reference to the webcam
if not input_video:
    camera = cv2.VideoCapture(0)
    time.sleep(2)
else:
    camera = cv2.VideoCapture(input_video)

faceutil = FaceUtil(facial_recognition_model_path)


# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a videos and we did not grab a frame, then we
    # have reached the end of the videos
    if input_video and not grabbed:
        break

    if not input_video:
        frame = cv2.flip(frame, 1)

    # resize the frame, convert it to grayscale, and then clone the
    # original frame so we can draw on it later in the program
    frame = imutils.resize(frame, width=600)

    face_location_list, names = faceutil.get_face_location_and_name(
        frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # loop over the faces bounding boxes
    for ((left, top, right, bottom), name) in zip(
            face_location_list,
            names):
        # extract the ROI of the faces from the grayscale image,
        # resize it to a fixed 28x28 pixels, and then prepare the
        # ROI for classification via the CNN
        roi = gray[top:bottom, left:right]
        roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH,
                               FACIAL_EXPRESSION_TARGET_HEIGHT))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        # determine facial expression
        (neural, smile) = model.predict(roi)[0]
        label = "Neural" if neural > smile else "Smile"

        # display the label and bounding box rectangle on the output
        # frame
        cv2.putText(frame, name + " is"  +  label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 0, 255), 2)

    # show our detected faces along with smiling/not smiling labels
    cv2.imshow("Facial Expression Detect", frame)

    # Press 'ESC' for exiting videos
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
