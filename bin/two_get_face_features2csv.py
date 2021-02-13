# -*- coding:utf-8 -*-

import os
import sys
import cv2
import csv
import dlib
import numpy
import pandas
import skimage
from one_get_face_form_camera import *
from skimage import io as iio
from golbalvar import *
from face_op import *
from sql import *

#初始化检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor_68_face_landmarks_path)
facerec = dlib.face_recognition_model_v1(dlib_face_recognition_resnet_model_v1_path)

def get_128D_features(img_path):
    """
    接受人脸图像路径,
    返回给定图片的128D特征
    :param img_path: 接受检测的图片的路径
    """
    img = iio.imread(img_path, 0)                                                            #读入图片，加载灰度
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)                                                            #放大检测图片，提升精度

    if (len(faces) !=0):                                                                     #如果检测到人脸
        shape = predictor(img_gray, faces[0])                                                #68关键点转128D面部描述len符
        face_descriptor = facerec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0 
    
    return face_descriptor

def compute_mean_value(erlist):
    """
    传入二维数组
    计算人脸特征均值并返回
    """
    print("数据长度" + str(len(erlist)))
    if erlist != 0:                                                                          #如果存在数据
        feature_mean_list = []                                                                #均值列
        for i in range(128):
            feature_mean_list.append(0)
            for j in range(len(erlist)):
                feature_mean_list[i] += erlist[j][i]
            feature_mean_list[i] = (feature_mean_list[i] / len(erlist))
    else:
        print("Warning: no data column in file")
        feature_mean_list = []

    return feature_mean_list

def demo(user):

    #进入目录生成二维数组
    user_dir = path_photos_from_camera  + user
    list1 = []
    faces = os.listdir(user_dir)
    if faces != 0:
        for person in faces:
            features_128D = get_128D_features(user_dir + "\\" + person)
            if features_128D == 0:                                                        #如果没有检测出人脸，跳过，否则写入一行
                continue
            else:
                list1.append(features_128D)
    else:
        print("目标目录为空！")

    #人脸均值计算, 写入数据库
    feature_mean_list = compute_mean_value(list1)
    print(len(feature_mean_list))
    print("-------------------------------------------------------")
    print(feature_mean_list)

    conn = create_sqlite3(FACE_SQL_NAME)
    ret = face_insert(conn, user, feature_mean_list)
    if ret == True:
        print("ok")
    else:
        print("no")

