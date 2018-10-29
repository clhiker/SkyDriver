'''2.创建一个item'''
# -*- coding: utf-8 -*-
# 创建一个矩形，指定画布的颜色为白色
from tkinter import *

root = Tk()
# 创建一个Canvas，设置其背景色为白色
cv = Canvas(root, bg='white')
# 创建一个矩形，坐标为(10,10,110,110)
cv.create_rectangle(10, 10, 110, 110)

'''3.指定item的填充色'''
# 指定矩形的填充色为红色
cv.create_rectangle(120, 10, 220, 110, fill='red')

'''4.指定item的边框颜色'''
# 指定矩形的边框颜色为红色
cv.create_rectangle(10, 120, 110, 220, outline='red')

'''5.指定边框的宽度'''
# 指定矩形的边框颜色为红色，设置线宽为5，注意与Canvas的width是不同的。
cv.create_rectangle(120, 120, 220, 220, outline='red', width=5)
cv.pack()
Button(root, text='hhda').pack()

root.mainloop()
# 为明显起见，将背景色设置为白色，用以区别root