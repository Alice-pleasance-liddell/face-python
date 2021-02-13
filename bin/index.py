# -*- coding: utf-8 -*-

import os
import PIL.Image
import data_operate as data_query
import one_get_face_form_camera as get_photos
import three_face_distinguish_from_camera as distinguish
from PIL import ImageTk
from sql import init_data
from tkinter import *

#窗口大小与背景图
FRAME_SIZE = "400x600"
WEC_IMG = "../data/index.jpg"
#按钮颜色
bg = "#5b7da0"
fg = "#000000"

def recon_img():
    """
    人脸识别按钮跳转
    """
    distinguish.demo()
    pass

def take_photo():
    """
    人脸注册跳转
    """
    get_photos.demo()
    pass

def data_op():
    """
    数据操作跳转
    """
    data_query.demo()
    pass

def quit_py(app):
    """
    结束程序
    """
    app.destroy()

def create_window():

    init_data()

    app = Tk()
    app.title("基于python的人脸识别")
    app.geometry(FRAME_SIZE)
    app.configure(bg = "black")
    app.resizable(0, 0)

    wec_image = PIL.Image.open(WEC_IMG).resize((400, 300))
    img = ImageTk.PhotoImage(wec_image)
    label = Label(app, image = img, bg ="black")
    label.pack()

    # 建立上层框架
    frame_upper = Frame(app, bg = "black")
    frame_upper.pack(pady = 15)

    scan_button = Button(frame_upper, bg = bg, fg = fg, text = "人脸识别", width = 24, height = 3, command = lambda: recon_img())
    scan_button.pack(side = LEFT, padx = 15, pady = 25)

    add_button = Button(frame_upper, bg = bg, fg = fg, text = "人物注册", width = 24, height = 3, command = lambda: take_photo())
    add_button.pack(side = LEFT, padx = 15, pady = 25)

    # 建立下层框架
    frame_lower = Frame(app, bg = "black")
    frame_lower.pack(pady = 5)

    del_button = Button(frame_lower, bg = bg, fg = fg, text = "数据操作", width = 24, height = 3, command = lambda: data_op())
    del_button.pack(side = LEFT, padx = 15, pady = 25)

    face_rec_button = Button(frame_lower, bg = bg, fg = fg, text = "退出", width = 24, height = 3, command = lambda: quit_py(app))
    face_rec_button.pack(side = LEFT, padx = 15, pady = 25)

    app.mainloop()

if __name__ == '__main__':
    create_window()