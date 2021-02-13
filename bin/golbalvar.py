#-*- coding:utf8 -*-

import os
import sys

shape_predictor_68_face_landmarks_path = os.path.abspath(os.path.join(os.getcwd(), "../lib")) + '\shape_predictor_68_face_landmarks.dat'
dlib_face_recognition_resnet_model_v1_path = os.path.abspath(os.path.join(os.getcwd(), "../lib")) + '\dlib_face_recognition_resnet_model_v1.dat'
path_photos_from_camera = os.path.abspath(os.path.join(os.getcwd(), "../data")) + '\data_faces_from_camera\\'
path_csvs_from_photos = os.path.abspath(os.path.join(os.getcwd(), "../data")) + '\data_csvs_from_camera\\'
all_features_csv_path = os.path.abspath(os.path.join(os.getcwd(), "../data")) + '\\features_all.csv'
