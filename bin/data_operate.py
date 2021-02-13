# -*- coding:utf-8 -*-

import sys
import tkinter
import tkinter.ttk
import tkinter.messagebox
from one_get_face_form_camera import getuser
from golbalvar import *
from face_op import *
from tkinter import *
from sql import *

user_name = ""

def query_data(user_text, tree):
	global user_name

	user_name = getuser(user_text)

	if user_name is None or user_name == '':
		tkinter.messagebox.showinfo("警告", "查询条件不能为空！")
		return False
	else:
		result = face_query_by_name(sql_con(), user_name)

		if not result:
			tkinter.messagebox.showinfo("警告", "查询结果为空！")
		else:
			for _ in map(tree.delete, tree.get_children("")):
				continue
			for i in result:
				tree.insert("", "end", values=(i[0],i[1],i[2]))

def del_data():
	global user_name

	if user_name is None or user_name == '':
		tkinter.messagebox.showinfo("警告", "删除条件不能为空！")
		return False
	else:
		face_del_by_name(sql_con(), user_name)
		print("ok")

def demo():

	root = tkinter.Toplevel()
	root.title("数据操作")
	root.geometry("300x400")
	root.resizable(0, 0)
	
	#上中下布局
	frame_top = tkinter.Frame(root, width = 300, height = 100, bg = "#000000")
	frame_center = tkinter.Frame(root, width = 300, height = 200, bg = "#000000")
	frame_bottom = tkinter.Frame(root, width = 300, height = 100, bg = "#000000")

	#表格与滚动条
	tree = ttk.Treeview(frame_center,show = "headings", height = 10, columns = ("a", "b", "c"))#表格
	vbar = ttk.Scrollbar(frame_center, orient = tkinter.VERTICAL, command = tree.yview)
	tree.configure(yscrollcommand=vbar.set)
	#表格布局
	tree["columns"] = ("ID", "NAME", "FACE_FEATURE")
	tree.column("ID", width = 50)   #表示列,不显示
	tree.column("NAME", width = 70)
	tree.column("FACE_FEATURE", width = 150)
	tree.heading("ID", text = "ID")  #显示表头
	tree.heading("NAME", text = "NAME")
	tree.heading("FACE_FEATURE", text = "FACE_FEATURE")

	tree.grid(row=0, column=0, sticky=tkinter.NSEW, ipadx=5)
	vbar.grid(row=0, column=1, sticky=tkinter.NS)
	
	#为列表插入数据
	cur = face_query_all(sql_con())
	line = 0
	for i in cur:
		tree.insert("",line,values=(i[0],i[1],i[2]))
		line += 1

	#顶部布局
	label1 = Label(frame_top, text = "姓 名:", fg = "#000000")
	user_text = Entry(frame_top, bg = "#FFFFFF")
	query_button = Button(frame_top, bg = "#5b7da0",fg = "#000000", text = "查询", width = 10, command = lambda: query_data(user_text, tree))
	label1.grid(row = 0, column = 0, padx= 15, pady = 30)
	user_text.grid(row = 0, column = 1, padx= 5, pady = 30)
	query_button.grid(row = 0, column = 2, padx = 10, pady = 30)

	#底部布局
	del_button = Button(frame_bottom, bg = "#5b7da0", fg = "#000000", text = "删除", width = 10, command = lambda: del_data())
	modify_button = Button(frame_bottom, bg = "#5b7da0", fg = "#000000", text = "修改", width = 10)
	del_button.grid(row = 0, column = 0, padx = 40, pady = 30)
	modify_button.grid(row = 0, column = 1, padx = 40, pady = 40)

	frame_top.pack(side="top", fill = "both")
	frame_center.pack(fill="both")
	frame_bottom.pack(side="bottom", fill = "both")

	root.mainloop()

if __name__ == '__main__':
	demo()