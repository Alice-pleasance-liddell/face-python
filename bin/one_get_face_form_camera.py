# -*- coding:utf-8 -*-

import os
import cv2
import sys
import dlib
import shutil
import PIL.Image
import PIL.ImageTk
import numpy as np
import tkinter as tk
import two_get_face_features2csv as Tofeature
from golbalvar import *
from tkinter import *

new_face_dir = ""   #新注册的人脸图像文件夹
count_face_capture = 0         #人脸截图计数
WEC_IMG = "../data/index.jpg"
user = ""
detector = dlib.get_frontal_face_detector()  #人脸分类器
predictor = dlib.shape_predictor(shape_predictor_68_face_landmarks_path)  #人脸68点特征预测器

def found_face_dir():
    """
    发现或创建保存总人脸的文件夹
    """
    if os.path.isdir(path_photos_from_camera): 
    	print("Image directory found")
    else:
        os.mkdir(path_photos_from_camera)
        print("Image directory created")
    
def del_face_dir():
    """ 
    删除之前存在的人脸图像文件夹
    """
    # folders_rd = os.listdir(path_photos_from_camera)
    # for i in range(len(folders_rd)):
    # 	shutil.rmtree(path_photos_from_camera + folders_rd[i])

def draw_rectangle(faces,img_rd):
    """
    画矩形框
    """
    for k, v in enumerate(faces):                       #枚举人脸，绘制矩形框
        cv2.rectangle(img_rd, tuple([v.left(), v.top()]), tuple([v.right(), v.bottom()]), (0, 255, 255), 2)

def sava_csv_information():
    """
    人脸特征写入csv中每行存放一张人脸的信息，格式为：
    image_name,part_0_x,part_0_y,part_1_x,part_1_y,...,part_67_x,part_67_y
    """
    # with open(path_csvs_from_photos + 'person.csv', 'a', newline = '') as csvfile:
    # 	num_landmarks = 68   #循环68点
    # 	csv_write = csv.write(csvfile)
    # 	header = ['image_name']
    # 	# 写入一行
    # 	for i in range(num_landmarks):
    #         header += ['part_{}_x'.format(i), ' part_{}_y'.format(i)]
    #         csv_write.writerow(header)

    #         f = open('person.csv')
    #         imgs = f.readlines()      #返回一个列表    带换行符

    #         for img_path in imgs:
    #             img_path = os.path.join(paht_csvs_from_photos, img_path)
    #             print('img_path: '+img_path)
    #             real_img_path = img_path.strip('\n')

    #             img = cv2.imread(real_img_path)
    #             img = cv2.resize(img, (256, 256))
    #             dets = detector(img, 1)

    #             if len(dets) == 1:
    #                 row = [real_img_path.split('/')[-1]]
    #                 d = dets[0]
    #                 shape = predictor(img, d)
    #                 for i in range(num_landmarks):
    #                     part_i_x = shape.part(i).x
    #                     part_i_y = shape.part(i).y
    #                     row += [part_i_x, part_i_y]
    #                     csv_write.writerow(row)

def create_new_dir(root, user_name, new_dir_button):
    """
    创建新注册的人脸文件夹，并将状态改为不可用
    :param user_name:新人脸名
    :param new_dir_button:创建新文件夹的按钮
    """
    global new_face_dir
    global user

    if user == "":
        tips(root, num = 1)
        return FALSE

    for exsit_name in (os.listdir(path_photos_from_camera)):
        if user_name == exsit_name:
            user = ''
            tips(root, num = 2)
            
            return FALSE

    new_face_dir = path_photos_from_camera + str(user_name)
    os.makedirs(new_face_dir)
    disable_action(new_dir_button)
    print("New face folder:", new_face_dir)

def getuser(user_text):
    """
    获取文本框内容
    """
    global user

    user = user_text.get()

    return user

def disable_action(btn):
    btn.config(state=tk.DISABLED)
    btn['text']="已操作"

def save_photos(img_rd, save_photo, root):
    """
    保存当前图像至文件夹
    """
    global count_face_capture
    global new_face_dir
    
    count_face_capture += 1
    cv2.imencode('.jpg', img_rd)[1].tofile(str(new_face_dir) +'\\img_face' + str(count_face_capture) + '.jpg')
    print("Written:", str(new_face_dir) + '\img_face_' +str(count_face_capture) + '.jgp')
    if count_face_capture == 60:
        new_face_dir = ""
        disable_action(save_photo)
        tips2(root)

def tips(root, num):
    if num == 1:
        text = "请先输入要注册的名字"
    elif num == 2:
        text = "该人物已存在"

    label3 = Label(root, text=text, bg="#000000", fg="#FFFFFF")
    label3.place(x=200, y=20)

def tips2(root):
    label3 = Label(root, text="已达最大存储数量", bg="#000000", fg="#FFFFFF")
    label3.place(x=200, y=70)

def callback(root):
    Tofeature.demo(user)
    root.destroy()
    
def quit_py(root):
    """
    销毁窗口
    """
    root.destroy()

def demo():
    #初始化
    found_face_dir()
    global new_face_dir
    global user

    root = tk.Toplevel()
    root.title("获取人脸照片")
    root.geometry("360x400")
    root.resizable(0, 0)

    canvas = Canvas(root, width=600,height=400,bg="black")

    label1 = Label(root, text="姓 名:", bg="#000000", fg="#FFFFFF")
    user_text = Entry(root, bg="#FFFFFF")
    label1.place(x=23, y=20)
    user_text.place(x=70,y=20)

    new_dir_button = Button(root, bg="#5b7da0",fg="#000000", text="新建人物文件夹", width=24, command=lambda: create_new_dir(root, getuser(user_text), new_dir_button))
    new_dir_button.place(x=40,y=50)

    save_photo = Button(root, bg="#5b7da0",fg="#000000", text="拍摄图片", width=24, state=tk.DISABLED, command=lambda: save_photos(img_rd, save_photo, root))
    save_photo.place(x=40,y=70)

    commit_button = Button(root, bg="#5b7da0",fg="#000000", text="提交录入", state=tk.DISABLED, width=24, command=lambda: callback(root))
    commit_button.place(x=40,y=90)

    quit_button = Button(root, bg="#5b7da0",fg="#000000", text="返    回", width=24, command=lambda: quit_py(root))
    quit_button.place(x=40,y=110)

    #摄像机
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)

    while cap.isOpened():

        flag, img_rd = cap.read()#按帧读取    返回标识,三维矩阵
        img_rd=cv2.resize(img_rd,(0,0),fx=0.5,fy=0.5,interpolation=cv2.INTER_NEAREST)
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)#灰度处理，便于运算
        faces = detector(img_gray, 0)#正向人脸检测，不放大，放回四点坐标

        cv2.putText(img_rd, "Current faces: " + str(len(faces)), (0, 10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (0, 205), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "N: New face folder", (0, 220), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "S: Save current face", (0, 235), cv2.FONT_HERSHEY_COMPLEX, 0.4, (169, 169, 169), 1, cv2.LINE_AA)

        #如果检测到人脸
        if len(faces) != 0:

            draw_rectangle(faces, img_rd)   #根据人脸画框
            if new_face_dir :
                save_photo.config(state=tk.NORMAL)
                commit_button.config(state=tk.NORMAL)

            cv2.putText(img_rd, "S: Save current face", (0, 235), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

        cov= cv2.cvtColor(img_rd,cv2.COLOR_RGB2BGR)
        img=PIL.Image.fromarray(cov)
        img=PIL.ImageTk.PhotoImage(img)
        canvas.create_image(20, 150, anchor=NW,image=img)
        canvas.pack()
        root.update_idletasks()
        root.update()

    #释放摄像机，关闭窗口。
    cap.release()
    cv2.destroyAllWindows()

    root.mainloop()

if __name__ == "__main__":
    demo()
