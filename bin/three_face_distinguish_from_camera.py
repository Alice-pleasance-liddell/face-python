# -*- coding:utf8 -*-

import io
import os
import sys
import cv2
import dlib
import zlib
import numpy
import pandas
import PIL.Image
import tkinter as tk
import face_recognition
from PIL import ImageDraw, ImageFont, ImageTk
from PyFaceDet import facedetectcnn
from golbalvar import *
from io import BytesIO
from tkinter import *
from sql import *

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor_68_face_landmarks_path)
facerec = dlib.face_recognition_model_v1(dlib_face_recognition_resnet_model_v1_path)
font = ImageFont.truetype(os.path.abspath(os.path.join(os.getcwd(), "../lib")) + "\simsun.ttc", 30, encoding = 'utf-8')
#从数据库中提取的已知的数据
knew_id = []
knew_name = []
knew_face_feature = []

def draw_person_name(num,img_rd,faces,face_position_list,face_name):
    """
    绘制名字
    :param faces:检测到的人脸 
    :param img_rd:帧图像
    """
    for i in range(len(faces)):
        img_rd = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
        pilimg = PIL.Image.fromarray(img_rd)
        draw = ImageDraw.Draw(pilimg)
        print("ok")
        draw.text(face_position_list[num], face_name, (0, 255, 2255), font = font)
        img_rd = cv2.cvtColor(numpy.array(pilimg), cv2.COLOR_BGR2RGB)

def return_euclidean_distance(feature_1, feature_2):
    """
    计算两个128D向量间的欧式距离
    :param feature_1 feature_2:两个特征向量
    :return:返回比较结果
    """
    feature_1 = numpy.array(feature_1)
    feature_2 = numpy.array(feature_2)
    numpy.linalg.norm(feature_1 - feature_2)
    dist = numpy.sqrt(numpy.sum(numpy.square(feature_1 - feature_2)))

    if dist >0.4:
        return 0
    else:
        return 1

def get_face_128D_features(img_gray):
    """
    返回当前灰度图像的多个人脸128D特征
    :param img_gray:灰度图片
    :return:返回t特征列表
    """
    faces = detector(img_gray, 1)

    if len(faces) != 0:
        face_feature = []
        for i in range(len(faces)):
            shape = predictor(img_gray, faces[i])
            face_feature.append(facerec.compute_face_descriptor(img_gray, shape))
    else:
        face_feature = []

    return face_feature

def draw_rectangle(img_rd, faces):
    """
    绘制矩形框和名字
    :param faces:检测到的人脸
    :param img_rd:帧图像
    """
    for k, v in enumerate(faces):
        cv2.rectangle(img_rd, tuple([v.left(), v.top()]), tuple([v.right(), v.bottom()]), (0, 255, 255), 2)

def draw_tips(img_rd, faces):
    """
    绘制提示信息
    :param:检测到的人脸 
    :param img_rd:帧图像
    """
    cv2.putText(img_rd, "Q: Quit", (0, 450), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Current faces: " + str(len(faces)), (0, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA) 

def convert_array(text):
    out = BytesIO(text)
    out.seek(0)

    dataa = out.read()
    # 解压缩数据流
    out = io.BytesIO(zlib.decompress(dataa))
    return numpy.load(out)

def loadDataBase():
    """
    加载数据库数据
    :return:返回数据库中存储的所有人脸特征
    """
    conn = create_sqlite3("face.db")
    cur = conn.cursor()

    global knew_face_feature
    global knew_id
    global knew_name

    sql = 'SELECT ID, NAME, FACE_FEATURE FROM FACE_INFO'
    cur.execute(sql)
    origin = cur.fetchall()
    for row in origin:
        knew_id.append(row[0])
        knew_name.append(row[1])
        knew_face_feature.append(convert_array(row[2]))

def demo():

    loadDataBase()#从数据库加载所有数据

    #摄像头
    cap = cv2.VideoCapture(0)
    cap.set(3, 400)
    timeF = 2                      #优化一 跳帧, 不知道有用没用
    i = 0

    while cap.isOpened():
        i += 1
        if not (i % timeF == 0):
            continue

        #存储当前镜头人物坐标/名字 默认未识别
        face_position_list = []
        face_name = "未识别"

        falg, img_rd = cap.read()
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
        faces = detector(img_gray, 1)
        key_input = cv2.waitKey(1)

        #打印提示信息
        draw_tips(img_rd, faces)

        if key_input == ord('q'):
            break

        if len(faces) != 0:
            draw_rectangle(img_rd, faces)
            crruent_face_feature = []

            for i in range(len(faces)):
                shape = predictor(img_rd, faces[i])         #68关键点转128
                crruent_face_feature.append(facerec.compute_face_descriptor(img_rd, shape))

            for k in range(len(faces)):#遍历当前图像中所有捕获的人脸
                face_position_list.append(tuple([faces[k].left(), int(faces[k].bottom()+ 20)]))#名字坐标

                for i in range(len(knew_face_feature)):#在特征库中匹配捕获到的某张脸的特征
                    compare = return_euclidean_distance(crruent_face_feature[k], knew_face_feature[i])

                    if compare == 1:
                        face_name = knew_name[i]

                #打印人名
                for i in range(len(faces)):
                    img_rd = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
                    pilimg = PIL.Image.fromarray(img_rd)
                    draw = ImageDraw.Draw(pilimg)
                    draw.text(face_position_list[k], face_name, (0, 255, 2255), font = font)
                    img_rd = cv2.cvtColor(numpy.array(pilimg), cv2.COLOR_BGR2RGB)
                

        cv2.namedWindow('facial recognition', cv2.WINDOW_NORMAL)
        cv2.imshow('facial recognition', img_rd)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    demo()